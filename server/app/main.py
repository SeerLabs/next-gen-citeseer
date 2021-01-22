import uvicorn as uvicorn
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
from routers import document_routes, elastic_routes
import requests
RECAPTCHA_SECRET_KEY = os.environ['RECAPTCHA_SECRET_KEY']
RECAPTCHA_API_ENDPOINT = "https://www.google.com/recaptcha/api/siteverify"
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


@app.middleware("http")
async def recaptcha_check(request: Request, call_next):
    if request.method == "OPTIONS":
        return
    token = request.headers['token']
    body = { "secret": RECAPTCHA_SECRET_KEY, "response": token}
    res = requests.post(url = RECAPTCHA_API_ENDPOINT, data = body).json()
    if res["success"] != True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="recaptcha failed"
        )
    res = await call_next(request)
    return res
    
@app.get("/")
def pong():
    return {"ping": "pong!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
