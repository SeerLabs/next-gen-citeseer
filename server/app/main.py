import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import document_routes, elastic_routes

app = FastAPI()

origins = [
    "http://localhost:3000",
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
    uvicorn.run(app, host="localhost", port=8000)