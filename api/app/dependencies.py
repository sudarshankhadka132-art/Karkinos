"""Application wide dependency wiring."""

from __future__ import annotations

import os
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from .services.embedding import EmbeddingClient
from .services.search import PgVectorSearchService, SearchService


DATABASE_URL_ENV = "DATABASE_URL"


@lru_cache
def _get_engine_url() -> str:
    database_url = os.getenv(DATABASE_URL_ENV)
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL environment variable must be set for the search service"
        )
    return database_url


@lru_cache
def _get_session_maker() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(_get_engine_url(), poolclass=NullPool, future=True)
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    session_factory = _get_session_maker()
    async with session_factory() as session:
        yield session


async def get_embedder() -> EmbeddingClient:
    return EmbeddingClient()


async def get_search_service(
    session: AsyncSession = Depends(get_session),
    embedder: EmbeddingClient = Depends(get_embedder),
) -> SearchService:
    return PgVectorSearchService(session=session, embedder=embedder)
