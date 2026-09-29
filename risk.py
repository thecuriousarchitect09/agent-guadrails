from policies import TOOL_POLICY


def calculate_risk(tool_name: str) -> str:

    policy = TOOL_POLICY.get(tool_name)

    if not policy:
        return "UNKNOWN"

    return policy["risk"]