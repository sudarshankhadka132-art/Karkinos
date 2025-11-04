from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_cancers() -> list[dict[str, str]]:
  return [
    {"id": "c_breast", "name": "Breast Cancer"},
    {"id": "c_lung", "name": "Non-Small Cell Lung Cancer"},
    {"id": "c_melanoma", "name": "Melanoma"}
  ]
