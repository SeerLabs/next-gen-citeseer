from fastapi import APIRouter
from starlette.responses import FileResponse
import requests
import json
from requests.adapters import HTTPAdapter
from io import BytesIO
from fastapi import Response

from starlette.responses import FileResponse
router = APIRouter()

f = open('/home/kzp5555/next-gen-citeseer/server/app/routers/data.json')
_dict_mappings = json.load(f)

def get_new_csxid(doi):
    if _dict_mappings.get(doi):
        return _dict_mappings.get(doi)
    else:
        return None

@router.get("/download")
def get_document(
    key: str = "c1t3s33r", type: str = "pdf", repid: str = "rep1", doi: str = ""
):
    print("received a request for ", doi, " ", type, " ", repid, " ", key)
    pdf_id = get_new_csxid(doi)
    print("pdf id ", pdf_id)
    new_url = 'https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=' + pdf_id
    print("new url ", new_url)
    response_content = requests.get(new_url).content
    response = Response(content=response_content, media_type="application/pdf")
    #response.headers["Content-Disposition"] = f"attachment; filename={pdf_id}.pdf"
    return response