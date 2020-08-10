import nltk
from elasticsearch_dsl import Nested, Search

from services.elastic_service import ElasticService
from services.elasticsearch_adapters import ClusterAdapter

from collections import Counter
from typing import List
from ingestion.text_utils import remove_accents, strip_punctuation
from ingestion.interfaces import CSXClusterer
from models.elastic_models import Author, Paper, Citation, Cluster
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

_author_ = "Sai Raghav Keesara"
_copyright_ = "Copyright 2020, Penn State University"
_license_ = ""
_version_ = "1.0"
_maintainer_ = "Sai Raghav Keesara"
_email_ = "sai@psu.edu"
_status_ = "Development"

nltk.download('stopwords')

stopwords_dict = Counter(stopwords.words("english"))
name_join_words = Counter(["van", "von", "der", "den", "di", "de", "le"])


class KeyMatcherClusterer(CSXClusterer):

    def __init__(self):
        self.key_generator = KeyGenerator()
        self.elastic_service = ElasticService()
        self.cluster_adapter = ClusterAdapter(self.elastic_service)

    def cluster_paper(self, paper: Paper) -> str:
        keys = self.key_generator.get_keys(paper.title, paper.authors)
        paper.cluster_id = self.cluster_adapter.cluster_paper(keys=keys, paper=paper)
        self._cluster_citations_for_paper(paper)
        return paper.cluster_id

    def recluster_paper(self, paper: Paper):
        pass

    def _cluster_citations_for_paper(self, paper: Paper):
        for citation in paper.citations:
            citation_keys = self.key_generator.get_keys(citation.title, citation.authors)
            citation.paper_id = paper.paper_id
            citation.cluster_id = self.cluster_adapter.cluster_citation(citation_keys, citation)
            self.cluster_adapter.relate_citing_clusters(citation.cluster_id, paper.cluster_id)
            # save the citation
            citation.save(using=self.elastic_service.get_connection())


class KeyGenerator:

    def get_keys(self, title: str, authors: List[Author]):
        keys = []
        title_keys = self._get_title_keys(title)
        author_keys = self._get_author_keys(authors)

        if len(title_keys) == 0 or len(author_keys) == 0:
            return keys

        for author_key in author_keys:
            for title_key in title_keys:
                keys.append(author_key + "_" + title_key)
        return keys

    def _get_title_keys(self, title: str):
        keys = []
        title = self._normalize_title(title)
        self._build_title_key(keys, title)
        offset_title = " ".join(title.split()[1:-1])
        if offset_title is not title and len(offset_title) > 1:
            self._build_title_key(keys, offset_title)
        self._build_title_key(keys, title)
        return keys

    def _get_author_keys(self, authors: List[Author]):
        author_keys = []
        if authors is None or len(authors) == 0:
            return author_keys
        self._normalize_authors(authors)
        for author in authors:
            if 'surname' in author:
                author_keys.append(author.surname)
        return author_keys

    @classmethod
    def _build_title_key(cls, keys: List[str], title: str):
        title = title.replace(" ", "")
        if len(title) > 30:
            title = title[:30]
        if len(title) >= 5:
            keys.append(title)

    @classmethod
    def _normalize_authors(cls, authors: Nested(Author)):
        for author in authors:
            if 'surname' not in author.to_dict(skip_empty=False):
                continue
            author.surname = author.surname.lower()
            remove_accents(author.surname)
            author.surname = ''.join([name for name in author.surname.split() if name not in name_join_words])
            strip_punctuation(author.surname)

    @classmethod
    def _normalize_title(cls, text: str):
        if text is None:
            return ""
        ps = PorterStemmer()
        text = text.lower()
        strip_punctuation(text)
        text = ' '.join([ps.stem(word) for word in text.split() if word not in stopwords_dict])
        return text.strip()
