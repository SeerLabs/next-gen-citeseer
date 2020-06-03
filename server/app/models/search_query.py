from typing import List

from pydantic import BaseModel


# TODO: Use this Model to convert /search API to post API instead of GET API
class SearchQuery(BaseModel):
    queryString: str
    page: int
    pageSize: int
