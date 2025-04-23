# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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


class EmailContent(BaseModel):
    Content: str
    ContentTemplateName: Optional[str]
    HtmlTemplateName: Optional[str]
