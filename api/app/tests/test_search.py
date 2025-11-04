from __future__ import annotations

import pytest
from httpx import AsyncClient

from api.app.main import create_app
from api.app.services.search import ChunkMatch, DocumentRef


class InMemorySearchService:
    def __init__(self, matches: list[ChunkMatch]) -> None:
        self._matches = matches

    async def search(self, query: str, top_k: int):
        # Basic guard to show the request was passed through correctly.
        assert query
        return self._matches[:top_k]


@pytest.fixture
async def api_client() -> AsyncClient:
    app = create_app()

    sample_matches = [
        ChunkMatch(
            chunk_id=1,
            text="Pembrolizumab is effective for PD-L1 positive NSCLC patients.",
            score=0.9123,
            document=DocumentRef(
                id=11,
                title="Checkpoint inhibitors in NSCLC",
                source="ASCO 2023",
                cancer_type="NSCLC",
            ),
        ),
        ChunkMatch(
            chunk_id=2,
            text="Consider osimertinib for EGFR exon 19 deletion mutations.",
            score=0.8344,
            document=DocumentRef(
                id=12,
                title="Targeted therapies in lung cancer",
                source="NCCN",
                cancer_type="Lung",
            ),
        ),
    ]

    service = InMemorySearchService(sample_matches)

    # Override the dependency to avoid hitting a real database in tests.
    from api.app import dependencies

    app.dependency_overrides[dependencies.get_search_service] = lambda: service

    client = AsyncClient(app=app, base_url="http://testserver")
    try:
        yield client
    finally:
        await client.aclose()
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_search_endpoint_returns_vector_matches(api_client: AsyncClient) -> None:
    response = await api_client.post(
        "/search",
        json={"query": "lung cancer", "top_k": 2},
    )

    assert response.status_code == 200
    payload = response.json()

    assert payload["query"] == "lung cancer"
    assert payload["top_k"] == 2
    assert len(payload["results"]) == 2

    first = payload["results"][0]
    assert first["chunk_id"] == 1
    assert "PD-L1" in first["text"]
    assert first["document"]["source"] == "ASCO 2023"
    assert first["document"]["cancer_type"] == "NSCLC"


@pytest.mark.asyncio
async def test_search_endpoint_validates_payload(api_client: AsyncClient) -> None:
    response = await api_client.post(
        "/search",
        json={"query": "", "top_k": 0},
    )

    assert response.status_code == 422
