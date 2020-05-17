from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(CORSMiddleware,
                       allow_origin_regex="http://localhost:*",
                       allow_credentials=True,
                       allow_headers=['*'])


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
