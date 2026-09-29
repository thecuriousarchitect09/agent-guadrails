from models import (
    Decision,
    GuardrailResult,
)

from tools import TOOLS
from policies import TOOL_POLICY

from permissions import user_can_use
from validators import (
    validate_arguments,
    validate_path,
)

from risk import calculate_risk
from approval import request_approval
from output_guard import validate_output
from audit import audit


class GuardrailEngine:

    def __init__(self, max_tool_calls=5):

        self.max_tool_calls = max_tool_calls
        self.tool_calls = 0

    # --------------------------------------------------------
    # CHECK
    # --------------------------------------------------------

    def check(self, user, call):

        # Runtime limit
        if self.tool_calls >= self.max_tool_calls:

            return GuardrailResult(
                Decision.BLOCK,
                "Maximum tool calls exceeded."
            )

        # Tool exists?
        if call.name not in TOOLS:

            return GuardrailResult(
                Decision.BLOCK,
                "Unknown tool."
            )

        # Policy exists?
        policy = TOOL_POLICY.get(call.name)

        if not policy:

            return GuardrailResult(
                Decision.BLOCK,
                "No policy defined."
            )

        # Explicitly blocked
        if policy.get("blocked"):

            return GuardrailResult(
                Decision.BLOCK,
                "Tool explicitly blocked."
            )

        # Permission
        if not user_can_use(
            user,
            call.name
        ):

            return GuardrailResult(
                Decision.BLOCK,
                "User lacks permission."
            )

        # Argument validation
        if not validate_arguments(call):

            return GuardrailResult(
                Decision.BLOCK,
                "Invalid arguments."
            )

        # Path validation
        if "path" in call.arguments:

            if not validate_path(
                call.arguments["path"]
            ):

                return GuardrailResult(
                    Decision.BLOCK,
                    "Unsafe path."
                )

        # Risk
        risk = calculate_risk(call.name)

        audit(
            "RISK_ASSESSMENT",
            tool=call.name,
            risk=risk,
        )

        # Human approval
        if policy.get("approval"):

            return GuardrailResult(
                Decision.APPROVAL_REQUIRED,
                f"{call.name} requires approval."
            )

        return GuardrailResult(
            Decision.ALLOW,
            "Action allowed."
        )

    # --------------------------------------------------------
    # EXECUTE
    # --------------------------------------------------------

    def execute(self, user, call):

        audit(
            "TOOL_REQUEST",
            user=user.name,
            tool=call.name,
            arguments=call.arguments,
        )

        decision = self.check(
            user,
            call
        )

        audit(
            "GUARDRAIL_DECISION",
            decision=decision.decision.value,
            reason=decision.reason,
        )

        # BLOCK
        if decision.decision == Decision.BLOCK:

            print(
                f"[BLOCKED] {decision.reason}"
            )

            return {
                "error": decision.reason
            }

        # APPROVAL
        if (
            decision.decision
            == Decision.APPROVAL_REQUIRED
        ):

            approved = request_approval(call)

            if not approved:

                audit(
                    "HUMAN_REJECTED",
                    tool=call.name,
                )

                return {
                    "error":
                    "Human rejected action."
                }

            audit(
                "HUMAN_APPROVED",
                tool=call.name,
            )

        # EXECUTE
        self.tool_calls += 1

        tool = TOOLS[call.name]

        result = tool(
            **call.arguments
        )

        audit(
            "TOOL_EXECUTED",
            tool=call.name,
        )

        # OUTPUT GUARD
        result = validate_output(result)

        audit(
            "OUTPUT_VALIDATED",
            tool=call.name,
        )

        return result