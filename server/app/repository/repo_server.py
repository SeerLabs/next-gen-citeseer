from typing import Optional

import uvicorn as uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

app = FastAPI()


# origins = [
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/document")
def get_pdf(doi: str, type: Optional[str] = "pdf", rep_id: Optional[str] = "1"):
    chunks = [doi[i:i + 2] for i in range(0, len(doi), 2)]
    filename = doi + "." + type
    pdf_repo_path = os.path.join("/data/repo/", chunks[0],
                                 chunks[1], chunks[2], chunks[3], chunks[4], chunks[5],
                                 chunks[6], doi, filename)
    return FileResponse(pdf_repo_path)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8889)
