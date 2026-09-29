def user_can_use(user, tool_name: str) -> bool:
    return user.can_use(tool_name)