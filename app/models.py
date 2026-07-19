from pydantic import BaseModel, Field
from app.statusEnum import Status
from typing import Any

class ResearchRequest(BaseModel):
    question: str = Field(..., description="The research objective or query.")
    require_approval: bool = Field(default=True, description="Whether human approval is required before saving reports.")


class ResearchResult(BaseModel):
    report_id: str = Field(..., description="Unique identifier for this run.")
    status: Status = "draft"
    result: str = Field(..., description="Human-readable final response.")
    tools_used: list[str] = Field(default_factory=list)
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    approved_to_save: bool = False
    latency_seconds: float = 0.0