import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from models.elastic_models import Cluster
from routers import document_routes, elastic_routes, authentication_routes
from fastapi_jwt_auth.exceptions import AuthJWTException
from services.elastic_service import ElasticService
from fastapi.responses import JSONResponse
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
app.include_router(authentication_routes.router, tags=['authentication_routes'], prefix="/api")
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.get("/")
def pong():
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
