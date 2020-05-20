from fastapi import APIRouter
from app.services.repository_service import RepositoryService

router = APIRouter()


@router.get('/document', response_model=None)
async def get_document(key: str = "c1t3s33r", type: str = "pdf", repid: str = "rep1", doi: str = ""):
    print(type)
    print(repid)
    print(doi)
    print(key)
    rep_svc = RepositoryService()
    rep_svc.get_document(doi=doi, file_type=type, repid=repid)
