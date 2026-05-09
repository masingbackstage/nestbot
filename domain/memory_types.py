from enum import Enum


class MemoryType(str, Enum):
    PROFILE = "profile"
    PREFERENCE = "preference"
    DECISION = "decision"
    PROJECT_CONTEXT = "project_context"
    DOCUMENT = "document"
