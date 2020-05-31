from typing import List

from pydantic import BaseModel

from models.paper import Paper


class SearchQueryResponse(BaseModel):
    query_id: str
    response: List[Paper]

class PaperDetailResponse(BaseModel):
    query_id: str
    response: Paper
