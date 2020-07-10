from typing import Optional, List

from pydantic import BaseModel, typing


class Paper(BaseModel):
    id: str
    title: str
    venue: str
    year: str
    n_citation: int
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