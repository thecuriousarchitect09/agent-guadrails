from models import (
    User,
    ToolCall,
)

from agent import Agent
from guardrails import GuardrailEngine


def main():

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    user = User(
        name="alice",

        permissions={
            "read_file",
            "write_file",
            "delete_file",
            "get_secret",
        },
    )

    # --------------------------------------------------------
    # GUARDRAILS
    # --------------------------------------------------------

    guardrails = GuardrailEngine(
        max_tool_calls=5
    )

    # --------------------------------------------------------
    # AGENT
    # --------------------------------------------------------

    agent = Agent(
        guardrails,
        user,
    )

    # ========================================================
    # TEST 1
    # ALLOW
    # ========================================================

    agent.run(
        ToolCall(
            name="read_file",

            arguments={
                "path": "/safe/report.txt"
            },
        )
    )

    # ========================================================
    # TEST 2
    # BLOCK
    # Unsafe path
    # ========================================================

    agent.run(
        ToolCall(
            name="delete_file",

            arguments={
                "path": "/etc/passwd"
            },
        )
    )

    # ========================================================
    # TEST 3
    # HUMAN APPROVAL
    # ========================================================

    agent.run(
        ToolCall(
            name="delete_file",

            arguments={
                "path":
                "/safe/old_report.txt"
            },
        )
    )

    # ========================================================
    # TEST 4
    # BLOCK
    # Explicitly blocked tool
    # ========================================================

    agent.run(
        ToolCall(
            name="get_secret",
            arguments={},
        )
    )


if __name__ == "__main__":
    main()