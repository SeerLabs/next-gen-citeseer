import tempfile

from fastapi import APIRouter
from starlette.responses import FileResponse
from services.repository_service import RepositoryService

router = APIRouter()
rep_svc = RepositoryService()


@router.get("/document")
def get_document(
    key: str = "c1t3s33r", type: str = "pdf", repid: str = "rep1", doi: str = ""
):
    # TODO: Implement a logging framework
    print("received a request for ", doi, " ", type, " ", repid, " ", key)
    response_content = rep_svc.get_document(
        doi=doi, file_type=type, repid=repid
    ).content
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as FOUT:
        FOUT.write(response_content)
        return FileResponse(FOUT.name, media_type="application/pdf")
