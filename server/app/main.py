import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import document_routes, elastic_routes

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://0.0.0.0:8080"
    "http://0.0.0.0:8000",
    "http://0.0.0.0:3000/",
    "http://istcsxfe01.ist.psu.edu"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_routes.router, tags=['document_routes'], prefix="/api")
app.include_router(elastic_routes.router, tags=['elastic_routes'], prefix="/api")

@app.get("/")
def pong():
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
