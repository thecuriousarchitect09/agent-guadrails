def validate_arguments(call) -> bool:

    if call.name == "read_file":
        return isinstance(
            call.arguments.get("path"),
            str
        )

    if call.name == "write_file":
        return (
            isinstance(
                call.arguments.get("path"),
                str
            )
            and
            isinstance(
                call.arguments.get("content"),
                str
            )
        )

    if call.name == "delete_file":
        return isinstance(
            call.arguments.get("path"),
            str
        )

    return True


def validate_path(path: str) -> bool:

    # Only allow /safe
    if not path.startswith("/safe/"):
        return False

    # Prevent traversal
    if ".." in path:
        return False

    return True