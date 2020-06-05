from typing import List
from uuid import uuid4

from fastapi import APIRouter

from models.api_response import SearchQueryResponse, PaperDetailResponse
from models.paper import Paper
from models.search_query import SearchQuery
from services.elastic_service import Elastic

router = APIRouter()
ES = Elastic()


@router.post('/search', response_model=SearchQueryResponse)
def perform_search(searchQuery: SearchQuery):
    docs_response = ES.paginated_search('citeseerx', searchQuery.queryString, searchQuery.page, searchQuery.pageSize,
                                        ['title', 'text'])
    result_list = []
    for doc_hit in docs_response['hits']['hits']:
        result_list.append(build_paper_entity(doc=doc_hit['_source']))
    total_results = docs_response['hits']['total']['value']
    return SearchQueryResponse(query_id=str(uuid4()), totalResults=total_results, response=result_list)


@router.get('/paper/{id}')
def paper_info(id: str):
    docs_response = ES.get_paper_info(id)
    paper_entity_response = build_paper_entity(docs_response['hits']['hits'][0]['_source'])
    return PaperDetailResponse(query_id=str(uuid4()), paper=paper_entity_response)


@router.get('/citations')
def citations(paperID: str = ""):
    result = ES.get_citations(paperID)
    return result


@router.get('/similar')
def similar_papers(paperID: str = ""):
    result = ES.get_clustered_papers(paperID)
    return result


def build_paper_entity(doc):
    return Paper(id=doc.get('paper_id'),
                 title=doc.get('title'),
                 venue=doc.get('venue'),
                 year=doc.get('year'),
                 n_citation=doc.get('ncites'),
                 abstract=doc.get('abstract'),
                 bibtex="test_bibtex",
                 authors=get_authors_in_list(doc, 'authors'),
                 journal=doc.get('journal'),
                 publish_time=doc.get('publish_time'),
                 source="")


def get_authors_in_list(doc, field) -> List[str]:
    return [field['name'] for field in doc[field]]
