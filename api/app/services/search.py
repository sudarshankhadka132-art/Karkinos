"""Database backed search service leveraging pgvector."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Protocol

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .embedding import EmbeddingClient


@dataclass
class DocumentRef:
    id: int
    title: str
    source: str
    cancer_type: str | None


@dataclass
class ChunkMatch:
    chunk_id: int
    text: str
    score: float
    document: DocumentRef


class SearchService(Protocol):
    async def search(self, query: str, top_k: int) -> Iterable[ChunkMatch]:
        """Search for the top matching knowledge chunks."""


class PgVectorSearchService:
    """Execute approximate nearest neighbour queries using pgvector."""

    def __init__(self, session: AsyncSession, embedder: EmbeddingClient) -> None:
        self._session = session
        self._embedder = embedder

    async def search(self, query: str, top_k: int) -> List[ChunkMatch]:
        query_vector = await self._embedder.embed(query)
        statement = text(
            """
            SELECT
                c.id AS chunk_id,
                c.body AS chunk_text,
                c.source AS chunk_source,
                c.document_id AS document_id,
                d.title AS document_title,
                d.source AS document_source,
                d.cancer_type AS cancer_type,
                1 - (c.embedding <#> :query_vector) AS similarity
            FROM knowledge_chunks c
            JOIN documents d ON d.id = c.document_id
            ORDER BY c.embedding <-> :query_vector
            LIMIT :top_k
            """
        )

        result = await self._session.execute(
            statement,
            {"query_vector": query_vector, "top_k": top_k},
        )

        matches: List[ChunkMatch] = []
        for row in result:
            matches.append(
                ChunkMatch(
                    chunk_id=row.chunk_id,
                    text=row.chunk_text,
                    score=float(row.similarity),
                    document=DocumentRef(
                        id=row.document_id,
                        title=row.document_title,
                        source=row.document_source,
                        cancer_type=row.cancer_type,
                    ),
                )
            )

        return matches
