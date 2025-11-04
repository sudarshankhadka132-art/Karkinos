"""Pydantic models for the search endpoint."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Free text query")
    top_k: int = Field(5, ge=1, le=50, description="Number of results to return")


class DocumentRefModel(BaseModel):
    id: int
    title: str
    source: str
    cancer_type: Optional[str]


class ChunkMatchModel(BaseModel):
    chunk_id: int
    text: str
    score: float
    document: DocumentRefModel


class SearchResponse(BaseModel):
    query: str
    top_k: int
    results: List[ChunkMatchModel]
