def request_approval(tool_call) -> bool:

    print()
    print("⚠️ HUMAN APPROVAL REQUIRED")
    print()
    print(f"Tool: {tool_call.name}")
    print(f"Arguments: {tool_call.arguments}")
    print()

    answer = input(
        "Approve this action? (yes/no): "
    )

    return answer.lower() == "yes"