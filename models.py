from dataclasses import dataclass
from enum import Enum
from typing import Any


class Decision(Enum):
    ALLOW = "allow"
    BLOCK = "block"
    APPROVAL_REQUIRED = "approval_required"


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass
class GuardrailResult:
    decision: Decision
    reason: str = ""


@dataclass
class User:
    name: str
    permissions: set[str]

    def can_use(self, tool_name: str) -> bool:
        return tool_name in self.permissions