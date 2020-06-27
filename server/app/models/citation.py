from pydantic import BaseModel, typing


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