from elasticsearch_dsl import Document, Text, Completion, Date, datetime, Keyword, Integer, Nested


class Author(Document):
    author_id: Text()
    author_suggest: Completion()
    forename: Text()
    surname: Text()
    affiliation: Text()
    address: Text()
    email: Keyword()
    ord: Integer()
    created_at = Date(default_timezone='UTC')

    class Index:
        name = 'authors'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)


class Citation(Document):
    citation_id = Text()
    title = Text()
    title_suggest = Completion()
    created_at = Date(default_timezone='UTC')
    authors = Nested(Author)

    class Index:
        name = 'citations'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)


class PaperKeyword(Document):
    keyword_id: Text()
    keyword: Text()

    class Index:
        name = 'keywords'


class Paper(Document):
    paper_id = Text()
    title = Text()
    cluster = Text()
    title_suggest = Completion()
    text = Text()
    abstract = Text()
    created_at = Date(default_timezone='UTC')
    authors = Nested(Author)
    citations = Nested(Citation)
    keywords = Nested(PaperKeyword)

    class Index:
        name = 'papers'

    def save(self, **kwargs):
        self.created_at = datetime.now()
        return super().save(**kwargs)
