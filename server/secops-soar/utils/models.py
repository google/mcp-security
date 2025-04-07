from enum import StrEnum


class CasePriority(StrEnum):
    PRIORITY_UNSPECIFIED = "PriorityUnspecified"
    PRIORITY_INFO = "PriorityInfo"
    PRIORITY_LOW = "PriorityLow"
    PRIORITY_MEDIUM = "PriorityMedium"
    PRIORITY_HIGH = "PriorityHigh"
    PRIORITY_CRITICAL = "PriorityCritical"
