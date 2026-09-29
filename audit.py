from datetime import datetime


def audit(event: str, **data):

    timestamp = datetime.now().isoformat()

    print(
        f"[AUDIT] {timestamp} "
        f"| {event} "
        f"| {data}"
    )