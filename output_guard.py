import re


SECRET_PATTERNS = [
    r"sk-[a-zA-Z0-9-]+",
    r"password\s*=\s*\S+",
    r"api[_-]?key\s*=\s*\S+",
]


def redact_secrets(value):

    if isinstance(value, dict):

        return {
            key: redact_secrets(val)
            for key, val in value.items()
        }

    if isinstance(value, list):

        return [
            redact_secrets(item)
            for item in value
        ]

    if isinstance(value, str):

        for pattern in SECRET_PATTERNS:

            value = re.sub(
                pattern,
                "[REDACTED]",
                value,
                flags=re.IGNORECASE,
            )

        return value

    return value


def validate_output(result):

    return redact_secrets(result)