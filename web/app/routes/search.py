"""Routes for the web search experience."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/intelligence/search", response_class=HTMLResponse)
async def search_page(request: Request) -> HTMLResponse:
    """Render the intelligence search UI."""

    return templates.TemplateResponse(
        "intelligence/search.html",
        {"request": request},
    )
