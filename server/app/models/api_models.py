from typing import List

from pydantic import BaseModel

from models.domain_models import Paper, Citation, Cluster


class SearchQueryResponse(BaseModel):
    query_id: str
    total_results: int
    response: List[Paper]

class PaperDetailResponse(BaseModel):
    query_id: str
    paper: Paper

class CitationsResponse(BaseModel):
    query_id: str
    total_results: int
    citations: List[Citation]

class ClusterDetailResponse(BaseModel):
    query_id: str
    cluster: Cluster

class showCitingClustersResponse(BaseModel):
    query_id: str
    total_results: int
    cluster: Cluster
    papers: List[Paper]

class SearchQuery(BaseModel):
    queryString: str
    page: int
    pageSize: int
