from enum import StrEnum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class CasePriority(StrEnum):
    PRIORITY_UNSPECIFIED = "PriorityUnspecified"
    PRIORITY_INFO = "PriorityInfo"
    PRIORITY_LOW = "PriorityLow"
    PRIORITY_MEDIUM = "PriorityMedium"
    PRIORITY_HIGH = "PriorityHigh"
    PRIORITY_CRITICAL = "PriorityCritical"


class TargetEntity(BaseModel):
    Identifier: str
    EntityType: str


class ApiManualActionDataModel(BaseModel):
    caseId: int
    targetEntities: List[Any] = Field(default_factory=list)
    properties: Dict[str, str] = Field(default_factory=dict)
    actionProvider: str
    actionName: str
    scope: Optional[str]
    alertGroupIdentifiers: List[str] = Field(default_factory=list)
    isPredefinedScope: bool
