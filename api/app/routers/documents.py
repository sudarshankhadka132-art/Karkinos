"""Document upload router."""
from __future__ import annotations

from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/documents")
async def upload_documents(files: List[UploadFile] = File(...)) -> dict:
    """Accept one or more documents and persist them to the raw data store.

    Args:
        files: Uploaded file objects provided by the client.

    Returns:
        A JSON payload containing the generated document identifiers.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files were provided")

    project_root = Path(__file__).resolve().parents[3]
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    document_ids: list[str] = []

    for upload in files:
        contents = await upload.read()
        if not contents:
            continue

        document_id = str(uuid4())
        sanitized_name = Path(upload.filename or "document").name
        target_path = raw_dir / f"{document_id}_{sanitized_name}"

        with target_path.open("wb") as fp:
            fp.write(contents)

        document_ids.append(document_id)

    if not document_ids:
        raise HTTPException(status_code=400, detail="All provided files were empty")

    return {"document_ids": document_ids}
