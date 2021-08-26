from typing import Optional

import uvicorn as uvicorn
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from starlette.responses import FileResponse

import settings
app = FastAPI()

@app.get("/document")
def get_pdf(doi: str, type: Optional[str] = "pdf", rep_id: Optional[str] = "1"):
    chunks = [doi[i:i + 2] for i in range(0, len(doi), 2)]
    filename = doi + "." + type
    pdf_repo_path = os.path.join(settings.REPO_SERVER_BASE_PATH, chunks[0],
                                 chunks[1], chunks[2], chunks[3], chunks[4], chunks[5],
                                 chunks[6], doi, filename)
    return FileResponse(pdf_repo_path)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.REPO_SERVER_HOST, port=8115)
