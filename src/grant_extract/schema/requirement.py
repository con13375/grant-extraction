from pydantic import BaseModel, Field
from typing import Literal, Optional, Union
from datetime import date


class Evidence(BaseModel):
    """A precise pointer back to the source document."""
    document_id: str
    section: Optional[str] = None
    span_start: int = Field(..., description="Character offset where the evidence begins")
    span_end: int = Field(..., description="Character offset where the evidence ends")


class Requirement(BaseModel):
    """A single requirement extracted from a grant document."""
    requirement_id: str
    type: Literal["boolean", "numeric", "date", "membership"]
    subject: str
    comparator: Optional[str] = None
    value: Optional[Union[str, int, float, date]] = None
    applicability: Optional[str] = None
    jurisdiction: str
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    evidence: Evidence  # Required. This is the point.
    exceptions: list[str] = []
    status: Literal["met", "unmet", "unknown"]
