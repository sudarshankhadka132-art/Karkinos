"""Search API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import get_search_service
from ..schemas.search import ChunkMatchModel, SearchRequest, SearchResponse
from ..services.search import ChunkMatch, SearchService

router = APIRouter(tags=["search"])


def _to_model(result: ChunkMatch) -> ChunkMatchModel:
    return ChunkMatchModel(
        chunk_id=result.chunk_id,
        text=result.text,
        score=result.score,
        document={
            "id": result.document.id,
            "title": result.document.title,
            "source": result.document.source,
            "cancer_type": result.document.cancer_type,
        },
    )


@router.post("/search", response_model=SearchResponse)
async def search(
    payload: SearchRequest,
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    """Execute an ANN search against the pgvector backed store."""

    matches = await search_service.search(payload.query, payload.top_k)
    models = [_to_model(match) for match in matches]
    return SearchResponse(query=payload.query, top_k=payload.top_k, results=models)
