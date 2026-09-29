def read_file(path: str):
    print(f"[TOOL] Reading: {path}")

    return {
        "path": path,
        "content": "This is a safe document."
    }


def write_file(path: str, content: str):
    print(f"[TOOL] Writing: {path}")

    return {
        "status": "success",
        "path": path
    }


def delete_file(path: str):
    print(f"[TOOL] DELETING: {path}")

    return {
        "status": "deleted",
        "path": path
    }


def get_secret():
    print("[TOOL] Reading secret")

    return {
        "api_key": "sk-super-secret-key-123"
    }


TOOLS = {
    "read_file": read_file,
    "write_file": write_file,
    "delete_file": delete_file,
    "get_secret": get_secret,
}