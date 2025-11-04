from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def search_documents(payload: dict[str, str]) -> dict[str, object]:
  query = payload.get("query", "")
  return {
    "query": query,
    "results": [
      {
        "document_id": "doc_placeholder",
        "chunk_id": "chunk_1",
        "score": 0.87,
        "text": "This is where a relevant oncology snippet would be returned."
      }
    ]
  }
