from typing import List

from elasticsearch_dsl import Document, Text, Completion, Date, datetime, Keyword, Integer, Nested, Boolean, InnerDoc


class Author(InnerDoc):
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
        name = 'authors'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        self.author_suggest = {
            'input': [self.forename, self.surname],
        }
        return super().save(**kwargs)


class PubInfo(InnerDoc):
    title: Text()
    date: Text()
    year: Integer()
    publisher: Text()
    meeting: Text()
    pub_place: Text()
    pub_address: Text()

    class Index:
        name = 'pub_info'

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

class KeyMap(Document):
    paper_id = Text()
    class Index:
        name = 'key_map'

class CorrectPaperMetadataES(Document):
    paper_id = Keyword()
    user_email = Keyword()
    title = Text()
    authors = Nested(Author)
    abstract = Text()
    pub_venue = Text()
    venue_type =Keyword()
    pub_year = Keyword()
    volume = Keyword()
    number = Keyword()
    pages = Keyword()
    publisher = Text()
    pub_address = Text()
    tech_report_num = Keyword()
    class Index:
        name = 'paper_metadata_correction_next'

class PaperMetadataCorrectionES(Document):
    user_email = Keyword()
    paper_id = Keyword()
    title = Text()
    authors = Nested(Author)
    abstract = Text()
    venue = Text()
    venue_type = Text()
    year = Integer()
    volume = Text()
    number = Text()
    pages = Text()
    publisher = Text()
    pub_address = Text()
    tech_report_num = Text()

    class Index:
        name = 'paper_metadata_correction_nextv1'


class Cluster(Document):
    paper_id = Keyword(multi=True)
    csx_doi = Keyword()
    title = Text()
    cluster_id = Keyword()
    title_suggest = Completion()
    text = Text()
    has_pdf = Boolean()
    abstract = Text()
    is_citation = Boolean()
    created_at = Date(default_timezone='UTC')
    authors = Nested(type='authors')
    self_cites = Integer()
    num_cites = Integer()
    cites = Keyword(multi=True)
    keys: Keyword(multi=True)
    keywords = Keyword(multi=True)
    pub_info = Nested(type='pub_info')

    class Index:
        name = 'acl_papers'

    def add_cites(self, paper_id: str):
        if not self.__contains__("cites"):
            self.__setitem__("cites", [paper_id])
            return
        self.cites.append(paper_id)
        self.modified_at = datetime.now()

    def get_cites(self):
        if not self.__contains__("cites"):
            return []
        else:
            return self.cites

    def get_paper_ids(self):
        if not self.__contains__("cites"):
            return []
        else:
            return self.paper_id

    def add_key(self, key: str):
        if not self.__contains__("keys"):
            self.__setitem__("keys", [key])
            return
        self.keys.append(key)
        self.modified_at = datetime.now()

    def add_paper_id(self, paper_id: str):
        if not self.__contains__("paper_id"):
            self.__setitem__("paper_id", [paper_id])
            return
        self.paper_id.append(paper_id)
        self.modified_at = datetime.now()

    def extend_keys(self, keys: List[str]):
        if not self.__contains__("keys"):
            self.__setitem__("keys", keys)
            return
        self.keys.extend(keys)
        self.modified_at = datetime.now()

    def save(self, **kwargs):
        self.created_at = datetime.now()
        if self.title is not None:
            self.title_suggest = {
                'input': [self.title],
            }
        return super().save(**kwargs)
