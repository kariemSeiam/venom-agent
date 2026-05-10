"""Pydantic models for validated SIPHON extraction payloads."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ExtractionSeverity(str, Enum):
    critical = "critical"
    major = "major"
    minor = "minor"
    info = "info"


class ExtractionEntry(BaseModel):
    timestamp: str = Field(description="ISO timestamp of the extraction")
    summary: str = Field(description="One-line summary of what happened")
    decision: str = Field(default="", description="Key decision made")
    correction: str = Field(default="", description="Correction received from user")
    pattern: str = Field(default="", description="Pattern observed")
    memory_worthy: bool = Field(default=False, description="Whether this should be stored in MEMORY.md")
    severity: ExtractionSeverity = Field(default=ExtractionSeverity.info)


class ExtractionResult(BaseModel):
    session_id: str
    extracted_at: datetime = Field(default_factory=datetime.now)
    entries: list[ExtractionEntry] = Field(default_factory=list)
    total_tokens: int = 0
    model_used: str = ""
