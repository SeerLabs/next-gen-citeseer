from typing import List

from pydantic import BaseModel

from models.citation import Citation
from models.cluster import Cluster
from models.paper import Paper


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
