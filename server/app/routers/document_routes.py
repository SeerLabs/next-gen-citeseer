import tempfile

from fastapi import APIRouter
from starlette.responses import FileResponse
from fastapi.responses import StreamingResponse

from services.repository_service import RepositoryService

router = APIRouter()


@router.get('/document')
def get_document(key: str = "c1t3s33r", type: str = "pdf", repid: str = "rep1", doi: str = ""):
    #TODO: Implement a logging framework
    print("recieved a request for ", doi, " ", type, " ", repid, " ", key)
    rep_svc = RepositoryService()
    response_content = rep_svc.get_document(doi=doi, file_type=type, repid=repid).content
    # return StreamingResponse(response, media_type="application/pdf")
    # print(response_content)
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".pdf", delete=False) as FOUT:
        FOUT.write(response_content)
        return FileResponse(FOUT.name, media_type="application/pdf")