from typing import List

from pydantic import BaseModel
from pydantic.class_validators import validator
from enum import Enum


class Document(BaseModel):
    id: str
    abstract: str = None
    authors: List[str] = []
    journal: str = None
    publish_time: str = None
    title: str
    source: str
    url: str
