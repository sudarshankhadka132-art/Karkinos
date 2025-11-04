from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


@router.post("/")
async def upload_document(
  source_id: Annotated[str, Form()],
  cancer_id: Annotated[str, Form()],
  title: Annotated[str, Form()],
  url: Annotated[str | None, Form()] = None,
  file: UploadFile | None = File(default=None)
) -> dict[str, str]:
  _ = file  # placeholder until storage is wired
  sha256 = "dummy-sha256"
  return {
    "id": "doc_placeholder",
    "source_id": source_id,
    "cancer_id": cancer_id,
    "title": title,
    "url": url or "https://example.org/document",
    "sha256": sha256,
    "created_at": datetime.utcnow().isoformat()
  }
