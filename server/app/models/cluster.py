from typing import Optional

from pydantic import BaseModel

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