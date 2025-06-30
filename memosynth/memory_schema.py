from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import date

class Memory(BaseModel):
    id: str
    project: str
    agent: str
    summary: str
    type: str
    tags: List[str]
    source: str
    author: str
    created_at: date
    version: int
    confidence: float = Field(..., ge=0.0, le=1.0)
    visibility: Literal["private", "project", "public"]
    sensitivity: Literal["low", "medium", "high"]
    topic: str
