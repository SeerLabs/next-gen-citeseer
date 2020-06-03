from typing import List

from pydantic import BaseModel

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
