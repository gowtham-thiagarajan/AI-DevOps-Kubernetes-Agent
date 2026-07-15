from typing import Any

from pydantic import BaseModel
from pydantic import Field


class HealthResponse(BaseModel):
    status: str
    service: str


class InvestigationPayload(BaseModel):
    pods: dict[str, Any] = Field(default_factory=dict)
    logs: dict[str, Any] = Field(default_factory=dict)
    events: dict[str, Any] = Field(default_factory=dict)
    deployments: dict[str, Any] = Field(default_factory=dict)
    network: dict[str, Any] = Field(default_factory=dict)


class DiagnosisPayload(BaseModel):
    root_cause: str
    explanation: str
    fix: str
    kubectl_command: str
    prevention: str
    confidence: int


class InvestigationResponse(BaseModel):
    status: str
    investigation: InvestigationPayload
    diagnosis: DiagnosisPayload | None = None
