from __future__ import annotations

import asyncio
import threading
import time
from typing import Iterable

import pytest
import uvicorn
from fastapi import FastAPI
from playwright.async_api import Page

from api.app.dependencies import get_search_service
from api.app.main import create_app as create_api_app
from api.app.services.search import ChunkMatch, DocumentRef, SearchService
from web.app.routes import search as search_routes


class StaticSearchService(SearchService):
    def __init__(self, matches: Iterable[ChunkMatch]) -> None:
        self._matches = list(matches)

    async def search(self, query: str, top_k: int):
        return self._matches[:top_k]


@pytest.fixture(scope="session")
def test_server() -> str:
    api_app = create_api_app()

    sample_matches = [
        ChunkMatch(
            chunk_id=21,
            text="Neoadjuvant chemotherapy improves pathological response in TNBC.",
            score=0.91,
            document=DocumentRef(
                id=201,
                title="TNBC management playbook",
                source="Karkinos KB",
                cancer_type="Breast",
            ),
        ),
        ChunkMatch(
            chunk_id=22,
            text="Carboplatin is recommended for BRCA1/2 mutation carriers.",
            score=0.83,
            document=DocumentRef(
                id=202,
                title="Inherited mutations guidance",
                source="ASCO",
                cancer_type="Breast",
            ),
        ),
    ]

    api_app.dependency_overrides[get_search_service] = lambda: StaticSearchService(sample_matches)

    combined = FastAPI()
    combined.include_router(api_app.router)
    combined.include_router(search_routes.router)

    config = uvicorn.Config(combined, host="127.0.0.1", port=8765, log_level="warning")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    timeout = time.time() + 10
    while not server.started and time.time() < timeout:
        time.sleep(0.05)

    if not server.started:
        raise RuntimeError("Uvicorn server failed to start for tests")

    try:
        yield "http://127.0.0.1:8765"
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        api_app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_search_user_flow(page: Page, test_server: str) -> None:
    await page.goto(f"{test_server}/intelligence/search")

    await page.fill("input[name=query]", "triple negative breast cancer")
    await page.click("#search-submit")

    await page.wait_for_selector('[data-testid="search-result"]')

    cards = await page.query_selector_all('[data-testid="search-result"]')
    assert cards, "Expected at least one search result to be rendered"

    title_text = await cards[0].query_selector_eval("h3", "el => el.textContent")
    assert "TNBC" in title_text or "Breast" in title_text

    meta_text = await cards[0].query_selector_eval(".result-meta", "el => el.textContent")
    assert "Source" in meta_text and "Cancer" in meta_text
