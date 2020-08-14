from typing import List
from uuid import uuid4

from fastapi import APIRouter

from models.api_models import SearchQueryResponse, PaperDetailResponse, CitationsResponse, ClusterDetailResponse, \
    showCitingClustersResponse, SearchQuery, Paper, Citation, Cluster, Aggregation, AggregationsResponse, AggregationBucket, AggregationsQuery

from services.elastic_service import ElasticService
from services.elasticsearch_adapters import PaperAdapter, CitationAdapter, ClusterAdapter

from utils.helpers import getKeyOrDefault

router = APIRouter()
elastic_service = ElasticService()
paper_adapter = PaperAdapter(elastic_service)
cluster_adapter = ClusterAdapter(elastic_service)
citation_adapter = CitationAdapter(elastic_service)


@router.post('/search/papers', response_model=SearchQueryResponse)
def perform_search(searchQuery: SearchQuery):
    docs_response = paper_adapter.search_papers(searchQuery)
    
    result_list = []
    for doc_hit in docs_response['hits']['hits']:
        result_list.append(build_paper_entity(doc=doc_hit['_source']))
    total_results = docs_response['hits']['total']['value']

    return SearchQueryResponse(query_id=str(uuid4()), total_results=total_results, response=result_list)


@router.post('/search/aggregations', response_model=AggregationsResponse)
def get_aggregations_from_query(aggsQuery: AggregationsQuery):

    response = paper_adapter.search_papers_aggregations(aggsQuery)

    aggregations = []
    for key in response:
      aggs_list = []
      for aggs in response[key]['buckets']:
        aggs_list.append(build_aggregations_entity(aggs))
      
      aggregations.append(AggregationBucket(key=key, items=aggs_list))
      
    return AggregationsResponse(query_id=str(uuid4()), aggs=aggregations)


@router.get('/paper/{id}')
def paper_info(id: str):
    docs_response = paper_adapter.get_paper_info(id)
    paper_entity_response = build_paper_entity(docs_response['hits']['hits'][0]['_source'])
    return PaperDetailResponse(query_id=str(uuid4()), paper=paper_entity_response)


@router.get('/citations/{id}')
def citations(id: str, page: int = 1, pageSize: int = 10):
    es_citations_response = citation_adapter.get_citations_for_paper(id, page, pageSize)
    result_list = []
    for doc_hit in es_citations_response['hits']['hits']:
        result_list.append(build_citation_entity(doc=doc_hit['_source']))
    total_results = es_citations_response['hits']['total']['value']
    return CitationsResponse(query_id=str(uuid4()), total_results=total_results, citations=result_list)


@router.get('/cluster/{cid}')
def show_cluster_detail(cid: str):
    cluster_detail_response = cluster_adapter.get_cluster_info(cid)
    return ClusterDetailResponse(query_id=str(uuid4()),
                                 cluster=build_cluster_entity(cluster_detail_response['_source']))


@router.get('/showCiting/{cid}')
def show_citing(cid: str, sort: str, page: int, pageSize: int):
    cluster_response = cluster_adapter.get_cluster_info(cid)
    primary_cluster_detail = build_cluster_entity(cluster_response['_source'])
    cid_list = cluster_response['_source']['cited_by']
    response = cluster_adapter.get_paper_ids_for_clusters(cid_list=cid_list)
    papers_list = []
    for each_hit in response['docs']:
        if 'included_papers' in each_hit['_source'] and len(each_hit['_source']['included_papers']) != 0:
            papers_list.append(each_hit['_source']['included_papers'][0])
    papers_response = paper_adapter.get_sorted_papers(papers_list=papers_list, page=page, pageSize=pageSize, sort=sort)
    result_list = []
    for each_paper_hit in papers_response['hits']['hits']:
        result_list.append(build_paper_entity(doc=each_paper_hit['_source']))
    total_results = papers_response['hits']['total']['value']
    return showCitingClustersResponse(query_id=str(uuid4()), total_results=total_results,
                                      cluster=primary_cluster_detail, papers=result_list)


@router.get('/similar')
def similar_papers(paperID: str = ""):
    result = cluster_adapter.get_clustered_papers(paperID)
    return result


def build_paper_entity(doc):
    return Paper(id=getKeyOrDefault(doc, 'paper_id'),
                 title=getKeyOrDefault(doc, 'title'),
                 venue=getKeyOrDefault(doc, 'venue'),
                 year=getKeyOrDefault(doc, 'year'),
                 n_cited_by=getKeyOrDefault(doc, 'ncites'),
                 n_self_cites=getKeyOrDefault(doc, 'selfCites'),
                 abstract=getKeyOrDefault(doc, 'abstract'),
                 bibtex="test_bibtex",
                 authors=get_authors_in_list(doc, 'authors'),
                 journal=getKeyOrDefault(doc, 'journal'),
                 publish_time=getKeyOrDefault(doc, 'publish_time'),
                 source="")

def build_aggregations_entity(aggs):
    return Aggregation(key=getKeyOrDefault(aggs, 'key'),
                        doc_count=getKeyOrDefault(aggs, 'doc_count'))

def get_authors_in_list(doc, field) -> List[str]:
    return [field['name'] for field in doc[field]]


def build_citation_entity(doc):
    return Citation(id=getKeyOrDefault(doc, 'id'),
                    cluster=getKeyOrDefault(doc, 'cluster'),
                    authors=getKeyOrDefault(doc, 'authors'),
                    title=getKeyOrDefault(doc, 'title'),
                    venue=getKeyOrDefault(doc, 'venue'),
                    venue_type=getKeyOrDefault(doc, 'venueType'),
                    year=getKeyOrDefault(doc, 'year'),
                    pages=getKeyOrDefault(doc, 'pages'),
                    editors=getKeyOrDefault(doc, 'editors'),
                    publisher=getKeyOrDefault(doc, 'publisher'),
                    pub_address=getKeyOrDefault(doc, 'pubAddress'),
                    volume=getKeyOrDefault(doc, 'volume'),
                    number=getKeyOrDefault(doc, 'number'),
                    tech=getKeyOrDefault(doc, 'tech'),
                    raw=getKeyOrDefault(doc, 'raw'),
                    paper_id=getKeyOrDefault(doc, 'paperid'),
                    self=getKeyOrDefault(doc, 'self'))


def build_cluster_entity(doc):
    return Cluster(cluster_id=getKeyOrDefault(doc, 'cluster_id'),
                   incollection=getKeyOrDefault(doc, 'incollection'),
                   cpublisher=getKeyOrDefault(doc, 'cpublisher'),
                   cyear=getKeyOrDefault(doc, 'cyear'),
                   observations=getKeyOrDefault(doc, 'observations'),
                   selfCites=getKeyOrDefault(doc, 'selfCites'),
                   ctitle=getKeyOrDefault(doc, 'ctitle'),
                   ctech=getKeyOrDefault(doc, 'ctech'),
                   cvol=getKeyOrDefault(doc, 'cvol'),
                   cvenue=getKeyOrDefault(doc, 'cvenue'),
                   cnum=getKeyOrDefault(doc, 'cnum'),
                   cpages=getKeyOrDefault(doc, 'cpages'),
                   cventype=getKeyOrDefault(doc, 'cventype'))