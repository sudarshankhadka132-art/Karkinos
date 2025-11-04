from fastapi import FastAPI

from .routers import cancers, documents, search, sources

app = FastAPI(title="Karkinos API", version="0.1.0")

app.include_router(sources.router, prefix="/sources", tags=["sources"])
app.include_router(cancers.router, prefix="/cancers", tags=["cancers"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
  return {"status": "ok"}
