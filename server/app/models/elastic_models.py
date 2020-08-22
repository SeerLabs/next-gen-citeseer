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

    def save(self, **kwargs):
        self.created_at = datetime.now()
        self.author_suggest = {
            'input': [self.forename, self.surname],
        }
        return super().save(**kwargs)


class PubInfo(Document):
    title: Text()
    date: Text()
    year: Integer()
    publisher: Text()
    meeting: Text()
    pub_place: Text()
    pub_address: Text()

    class Index:
        name = 'pub_info_next'

class CrawlMeta(Document):
    crawl_status: Boolean()
    pdf_path: Text()
    citations_extracted: Boolean()
    text_extracted: Boolean()
    source: Text()
    algorithms_extracted = Boolean()
    uid = Text()
    figures_extracted = Boolean()
    text_ingested = Boolean()
    time = Text()
    doi = Text()
    status = Boolean()
    # fields = Nested(Date)

    class Index:
        name = 'crawl_meta'

class Citation(Document):
    title = Text()
    title_suggest = Completion()
    created_at = Date(default_timezone='UTC')
    authors = Nested(Author)
    cluster_id = Keyword()
    in_collection = Boolean()
    paper_id = Text()
    raw = Text()
    pub_info = Nested(PubInfo)

    class Index:
        name = 'citations_next'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)


class Paper(Document):
    paper_id = Keyword()
    csx_doi = Keyword()
    title = Text()
    cluster_id = Keyword()
    title_suggest = Completion()
    text = Text()
    abstract = Text()
    created_at = Date(default_timezone='UTC')
    authors = Nested(Author)
    self_cites = Integer()
    num_cites = Integer()
    citations = Nested(Citation)
    keywords = Keyword(multi=True)
    pub_info = Nested(PubInfo)

    class Index:
        name = 'papers_next'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        self.title_suggest = {
            'input': [self.title],
        }
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

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)

    def add_paper_id(self, paper_id: str):
        if not self.__contains__("papers"):
            self.__setitem__("papers", [paper_id])
            return
        self.papers.append(paper_id)
        self.modified_at = datetime.now()

    def add_citation_id(self, citation_id: str):
        if not self.__contains__("citations"):
            self.__setitem__("citations", [citation_id])
            return
        self.citations.append(citation_id)
        self.modified_at = datetime.now()

    def add_cites(self, cite: str):
        if not self.__contains__("cites"):
            self.__setitem__("cites", [cite])
            return
        self.cites.append(cite)
        self.modified_at = datetime.now()

    def add_cited_by(self, cited_by: str):
        if not self.__contains__("cited_by"):
            self.__setitem__("cited_by", [cited_by])
            return
        self.cited_by.append(cited_by)
        self.modified_at = datetime.now()

    def add_key(self, key: str):
        if not self.__contains__("keys"):
            self.__setitem__("keys", [key])
            return
        self.keys.append(key)
        self.modified_at = datetime.now()

    def extend_keys(self, keys: List[str]):
        if not self.__contains__("keys"):
            self.__setitem__("keys", keys)
            return
        self.keys.extend(keys)
        self.modified_at = datetime.now()