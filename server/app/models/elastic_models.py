from typing import List

from elasticsearch_dsl import Document, Text, Completion, Date, datetime, Keyword, Integer, Nested, Boolean, InnerDoc


class Author(Document):
    author_suggest: Completion()
    cluster_id: Keyword()
    forename: Text()
    surname: Text()
    fullname: Text()
    affiliation: Text()
    address: Text()
    email: Keyword()
    ord: Integer()
    created_at = Date(default_timezone='UTC')

    class Index:
        name = 'authors_next'

    class Meta:
        doc_type = 'authors_next'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)


class PubInfo(Document):
    title: Text()
    monogr_title: Text()
    date: Text()
    publisher: Text()
    meeting: Text()

    class Index:
        name = 'pub_info_next'

    class Meta:
        doc_type = 'pub_info_next'


class Citation(Document):
    title = Text()
    title_suggest = Completion()
    created_at = Date(default_timezone='UTC')
    authors = Nested(Author)
    cluster_id = Keyword()
    paper_id = Text()
    raw: Text()
    pub_info = Nested(PubInfo)

    class Index:
        name = 'citations_next'

    class Meta:
        doc_type = 'citations_next'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)


class Paper(Document):
    paper_id = Text()
    title = Text()
    cluster_id = Keyword()
    title_suggest = Completion()
    text = Text()
    abstract = Text()
    created_at = Date(default_timezone='UTC')
    authors = Nested(Author)
    citations = Nested(Citation)
    keywords = Keyword(multi=True)
    pub_info = Nested(PubInfo)

    class Index:
        name = 'papers_next'

    class Meta:
        doc_type = 'papers_next'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)


class Cluster(Document):
    in_collection: Boolean()
    keys: Keyword(multi=True)
    citations: Keyword(multi=True)
    papers: Keyword(multi=True)
    title: Text()
    pub_info: Nested(PubInfo)
    authors: Nested(Author)
    cites: Keyword(multi=True)
    cited_by: Keyword(multi=True)
    created_at = Date(default_timezone='UTC')
    modified_at = Date(default_timezone='UTC')

    class Index:
        name = 'clusters_next'

    class Meta:
        doc_type = 'cluster_next'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)

    def add_paper_id(self, paper_id: str):
        self.papers.append(paper_id)
        self.modified_at = datetime.now()

    def add_citation_id(self, add_citation_id: str):
        self.citations.append(add_citation_id)
        self.modified_at = datetime.now()

    def add_cites(self, cite: str):
        self.cites.append(cite)
        self.modified_at = datetime.now()

    def add_cited_by(self, cited_by: str):
        self.cited_by.append(cited_by)
        self.modified_at = datetime.now()

    def add_key(self, key: str):
        self.keys.append(key)
        self.modified_at = datetime.now()

    def extend_keys(self, keys: List[str]):
        self.keys.extend(keys)
        self.modified_at = datetime.now()