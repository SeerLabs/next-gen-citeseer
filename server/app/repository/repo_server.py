from typing import Optional

import uvicorn as uvicorn
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
    return FileResponse("/data/repository/"+ doi[:2] + "/"+doi+"."+type)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8889)
