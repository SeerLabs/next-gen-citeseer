from typing import List

from pydantic import BaseModel

from models.paper import Paper


class SearchQueryResponse(BaseModel):
    query_id: str
    totalResults: int
    response: List[Paper]

class PaperDetailResponse(BaseModel):
    query_id: str
    paper: Paper
