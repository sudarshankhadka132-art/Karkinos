from datetime import datetime
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_sources() -> list[dict[str, str]]:
  return [
    {"id": "src_nccn", "name": "NCCN", "kind": "guideline", "created_at": datetime.utcnow().isoformat()},
    {"id": "src_asco", "name": "ASCO", "kind": "guideline", "created_at": datetime.utcnow().isoformat()},
    {"id": "src_esmo", "name": "ESMO", "kind": "guideline", "created_at": datetime.utcnow().isoformat()},
    {"id": "src_pmc", "name": "PubMed Central", "kind": "literature", "created_at": datetime.utcnow().isoformat()}
  ]
