from typing import List

from elasticsearch_dsl import Document, Text, Completion, Date, Keyword, Integer, Nested, Boolean, InnerDoc

import settings

'''
IMPORTANT: ANY UPDATES TO THIS FILE MUST ALSO BE MADE IN elastic_models.py
file of PDFMEF REPOSITORY AND VICE-VERSA
'''
class Author(InnerDoc):
    author_suggest = Completion()
    cluster_id = Keyword()
    forename = Text()
    surname = Text()
    fullname = Text()
    affiliation = Text()
    address = Text()
    email = Keyword()
    ord = Integer()
    created_at = Date(default_timezone='UTC')

    def save(self, **kwargs):
        self.author_suggest = {
            'input': [self.forename, self.surname],
        }
        return super().save(**kwargs)


class PubInfo(InnerDoc):
    title = Text()
    date = Text()
    year = Integer()
    publisher = Text()
    meeting = Text()
    pub_place = Text()
    pub_address = Text()


class KeyMap(Document):
    paper_id = Text()

    class Index:
        name = settings.KEYMAP_INDEX


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
    authors = Nested(Author)
    self_cites = Integer()
    num_cites = Integer()
    cited_by = Keyword(multi=True)
    keys = Keyword(multi=True)
    keywords = Keyword(multi=True)
    pub_info = Nested(PubInfo)

    class Index:
        name = settings.CLUSTERS_INDEX

    def add_cited_by(self, paper_id: str):
        if not self.__contains__("cited_by"):
            self.__setitem__("cited_by", [paper_id])
            return
        self.cited_by.append(paper_id)

    def get_cited_by(self):
        if not self.__contains__("cited_by"):
            return []
        else:
            return self.cited_by

    def get_paper_ids(self):
        if not self.__contains__("paper_id"):
            return []
        else:
            return self.paper_id

    def add_key(self, key: str):
        if not self.__contains__("keys"):
            self.__setitem__("keys", [key])
            return
        self.keys.append(key)

    def add_paper_id(self, paper_id: str):
        if not self.__contains__("paper_id"):
            self.__setitem__("paper_id", [paper_id])
            return
        self.paper_id.append(paper_id)

    def extend_keys(self, keys: List[str]):
        if not self.__contains__("keys"):
            self.__setitem__("keys", keys)
            return
        self.keys.extend(keys)

    def save(self, **kwargs):
        if self.title is not None:
            self.title_suggest = {
                'input': [self.title],
            }
        return super().save(**kwargs)


class UserRequest(Document):
    request_type = Keyword()
    requester_email = Keyword()
    requester_name = Keyword()
    reason_or_details = Text()
    paper_id = Keyword()
    title = Text()
    cluster_id = Keyword()
    abstract = Text()
    authors = Nested(Author)
    pub_info = Nested(PubInfo)
    status = Keyword()

    class Index:
        name = settings.REQUESTS_INDEX
