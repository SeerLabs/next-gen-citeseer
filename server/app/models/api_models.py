from typing import Optional, List, Dict

from pydantic import BaseModel, typing

class Author(BaseModel):
    name: str
    affiliation: Optional[str]
    address: Optional[str]
    email: Optional[str]

class Paper(BaseModel):
    id: Optional[str]
    title: Optional[str]
    venue: Optional[str]
    year: Optional[str]
    publisher: Optional[str]
    n_cited_by: Optional[int]
    n_self_cites: Optional[int]
    abstract: str = None
    bibtex: str
    authors: List[str] = []
    journal: str = None
    publish_time: str = None
    source: str
    urls: List[str] = []
    cluster_id: Optional[str]

class PublicationInfo(BaseModel):
    key: Optional[str]
    doc_count: Optional[int]

class Facets(BaseModel):
    pub_info_year_count: Optional[int]
    pub_info_year_list: List[PublicationInfo]
    pub_info_publisher_count: Optional[int]
    pub_info_publisher_list: List[PublicationInfo]
    authors_count: Optional[int]
    authors_fullname_terms: List[PublicationInfo]

class Citation(BaseModel):
    id: str
    cluster: Optional[str]
    authors: List[str] = []
    title: Optional[str]
    in_collection: Optional[bool]
    venue: Optional[str]
    venue_type: Optional[str]
    year: Optional[str]
    pages: Optional[str]
    editors: Optional[str]
    publisher: Optional[str]
    pub_address: Optional[str]
    volume: Optional[str]
    number: Optional[str]
    tech: Optional[str]
    raw: Optional[str]
    paper_id: Optional[str]
    self: Optional[str]

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


class PaperMetadataCorrection(BaseModel):
    id: str
    title: str
    authors: List[Author]
    abstract: str
    venue: str
    venue_type: str
    year: str
    volume:str
    number:str
    pages: str
    publisher: str
    pub_address: str
    tech_report_num: str
    
class Suggestion(BaseModel):
    type: str
    text: str
    id: str

class AutoCompleteResponse(BaseModel):
    query_id: str
    query: str
    suggestions: List[Suggestion]

class SearchQueryResponse(BaseModel):
    query_id: str
    total_results: int
    response: List[Paper]
    aggregations: Dict[str, Facets]

class SearchAuthorResponse(BaseModel):
    query_id: str
    total_results: int
    response:List[str]

class PaperDetailResponse(BaseModel):
    query_id: str
    paper: Paper

class CitationsResponse(BaseModel):
    query_id: str
    total_results: int
    citations: List[Citation]

class SimilarPapersResponse(BaseModel):
    query_id: str
    total_results: int
    similar_papers: List[Citation]

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
<<<<<<< HEAD
    yearStart: Optional[str]
    yearEnd: Optional[str]
    author: Optional[List[str]]
    publisher: Optional[List[str]]

class SearchFilter(BaseModel):
    queryString: str

class AggregationQuery(BaseModel):
    queryString: str

class AggregationResponse(BaseModel):
    aggregations: Dict[str, Facets]
=======

class MGetRequest(BaseModel):
    paper_id_list: List[str]


class UserRequest(BaseModel):
    paper_id: str
    reason_or_details: str
    title:str
    abstract: str
    authors: List[Author] 
    meeting: Optional[str]
    publisher: Optional[str]    
    publish_date: Optional[str]
    reviewer_comment: Optional[str]
class ProcessRequest(BaseModel):
    request_id: str
    reviewer_comment: str
class UserRequestResponse(BaseModel):
    request_id: str
    user_request: UserRequest
>>>>>>> dev
