from typing import List
from uuid import uuid4

from fastapi import APIRouter

from models.api_models import SearchQueryResponse, PaperDetailResponse, CitationsResponse, ClusterDetailResponse, \
    showCitingClustersResponse, SearchQuery
from models.domain_models import Paper, Citation, Cluster
from services.citation_dao import CitationDao
from services.cluster_dao import ClusterDao
from services.elastic_service import ElasticService
from services.paper_dao import PaperDao

router = APIRouter()
elastic_service = ElasticService()
paper_dao = PaperDao(elastic_service)
cluster_dao = ClusterDao(elastic_service)
citation_dao = CitationDao(elastic_service)


@router.post('/search', response_model=SearchQueryResponse)
def perform_search(searchQuery: SearchQuery):
    docs_response = paper_dao.search_papers(searchQuery)
    result_list = []
    for doc_hit in docs_response['hits']['hits']:
        result_list.append(build_paper_entity(doc=doc_hit['_source']))
    total_results = docs_response['hits']['total']['value']
    return SearchQueryResponse(query_id=str(uuid4()), total_results=total_results, response=result_list)


@router.get('/paper/{id}')
def paper_info(id: str):
    docs_response = paper_dao.get_paper_info(id)
    paper_entity_response = build_paper_entity(docs_response['hits']['hits'][0]['_source'])
    return PaperDetailResponse(query_id=str(uuid4()), paper=paper_entity_response)


@router.get('/citations/{id}')
def citations(id: str, page: int = 1, pageSize: int = 10):
    es_citations_response = citation_dao.get_citations_for_paper(id, page, pageSize)
    result_list = []
    for doc_hit in es_citations_response['hits']['hits']:
        result_list.append(build_citation_entity(doc=doc_hit['_source']))
    total_results = es_citations_response['hits']['total']['value']
    return CitationsResponse(query_id=str(uuid4()), total_results=total_results, citations=result_list)


@router.get('/cluster/{cid}')
def show_cluster_detail(cid: str):
    cluster_detail_response = cluster_dao.get_cluster_info(cid)
    return ClusterDetailResponse(query_id=str(uuid4()),
                                 cluster=build_cluster_entity(cluster_detail_response['_source']))


@router.get('/showCiting/{cid}')
def show_citing(cid: str, sort: str, page: int, pageSize: int):
    cluster_response = cluster_dao.get_cluster_info(cid)
    primary_cluster_detail = build_cluster_entity(cluster_response['_source'])
    cid_list = cluster_response['_source']['cited_by']
    response = cluster_dao.get_paper_ids_for_clusters(cid_list=cid_list)
    papers_list = []
    for each_hit in response['docs']:
        if 'included_papers' in each_hit['_source'] and len(each_hit['_source']['included_papers']) != 0:
            papers_list.append(each_hit['_source']['included_papers'][0])
    papers_response = paper_dao.get_sorted_papers(papers_list=papers_list, page=page, pageSize=pageSize, sort=sort)
    result_list = []
    for each_paper_hit in papers_response['hits']['hits']:
        result_list.append(build_paper_entity(doc=each_paper_hit['_source']))
    total_results = papers_response['hits']['total']['value']
    return showCitingClustersResponse(query_id=str(uuid4()), total_results=total_results,
                                      cluster=primary_cluster_detail, papers=result_list)


@router.get('/similar')
def similar_papers(paperID: str = ""):
    result = cluster_dao.get_clustered_papers(paperID)
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


def build_citation_entity(doc):
    return Citation(id=doc.get('id'),
                    cluster=doc.get('cluster'),
                    authors=doc.get('authors'),
                    title=doc.get('title'),
                    venue=doc.get('venue'),
                    venue_type=doc.get('venueType'),
                    year=doc.get('year'),
                    pages=doc.get('pages'),
                    editors=doc.get('editors'),
                    publisher=doc.get('publisher'),
                    pub_address=doc.get('pubAddress'),
                    volume=doc.get('volume'),
                    number=doc.get('number'),
                    tech=doc.get('tech'),
                    raw=doc.get('raw'),
                    paper_id=doc.get('paperid'),
                    self=doc.get('self'))


def build_cluster_entity(doc):
    return Cluster(cluster_id=doc.get('cluster_id'),
                   incollection=doc.get('incollection'),
                   cpublisher=doc.get('cpublisher'),
                   cyear=doc.get('cyear'),
                   observations=doc.get('observations'),
                   selfCites=doc.get('selfCites'),
                   ctitle=doc.get('ctitle'),
                   ctech=doc.get('ctech'),
                   cvol=doc.get('cvol'),
                   cvenue=doc.get('cvenue'),
                   cnum=doc.get('cnum'),
                   cpages=doc.get('cpages'),
                   cventype=doc.get('cventype'))