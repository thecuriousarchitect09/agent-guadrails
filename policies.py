TOOL_POLICY = {

    "read_file": {
        "risk": "LOW",
        "approval": False,
    },

    "write_file": {
        "risk": "MEDIUM",
        "approval": False,
    },

    "delete_file": {
        "risk": "HIGH",
        "approval": True,
    },

    "get_secret": {
        "risk": "CRITICAL",
        "approval": False,
        "blocked": True,
    },
}