from typing import Optional, List

from pydantic import BaseModel, typing


class Paper(BaseModel):
    id: Optional[str]
    title: Optional[str]
    venue: Optional[str]
    year: Optional[str]
    n_cited_by: Optional[int]
    n_self_cites: Optional[int]
    abstract: str = None
    bibtex: str
    authors: List[str] = []
    journal: str = None
    publish_time: str = None
    source: str
    urls: List[str] = []

class Citation(BaseModel):
    id: str
    cluster: int
    authors: typing.Any
    title: typing.Any
    venue: typing.Any
    venue_type: typing.Any
    year: typing.Any
    pages: typing.Any
    editors: typing.Any
    publisher: typing.Any
    pub_address: typing.Any
    volume: typing.Any
    number: typing.Any
    tech: typing.Any
    raw: str
    paper_id: str
    self: typing.Any

class Cluster(BaseModel):
    cluster_id: str
    incollection: int
    cpublisher: Optional[str]
    cyear: Optional[int]
    observations: Optional[str]
    selfCites: Optional[int]
    ctitle: Optional[str]
    ctech: Optional[str]
    cvol: Optional[str]
    cvenue: Optional[str]
    cnum: Optional[int]
    cpages: Optional[str]
    cventype: Optional[str]


class Aggregation(BaseModel):
    key: str
    doc_count: int

class AggregationBucket(BaseModel):
    key: str
    items: List[Aggregation]
    
class AggregationsResponse(BaseModel):
    aggs: List[AggregationBucket]

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

class YearFilter(BaseModel):
    start: int
    end: int

class QueryFilter(BaseModel):
    years: Optional[YearFilter]
    authors: Optional[List[str]]

class SearchQuery(BaseModel):
    queryString: str
    page: int
    pageSize: int
    filters: Optional[QueryFilter]

class AggregationsQuery(BaseModel):
    queryString: str
