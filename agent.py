from models import ToolCall


class Agent:

    def __init__(
        self,
        guardrails,
        user,
    ):

        self.guardrails = guardrails
        self.user = user

    def run(self, tool_call: ToolCall):

        print()
        print("=" * 60)
        print("AGENT")
        print("=" * 60)

        print(
            f"Requested tool: {tool_call.name}"
        )

        print(
            f"Arguments: {tool_call.arguments}"
        )

        result = self.guardrails.execute(
            self.user,
            tool_call,
        )

        print()
        print("RESULT:")
        print(result)

        return result