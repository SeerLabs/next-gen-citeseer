from typing import List
from uuid import uuid4

from fastapi import APIRouter

from models.api_models import SearchQueryResponse, PaperDetailResponse, CitationsResponse, ClusterDetailResponse, \
    showCitingClustersResponse, SimilarPapersResponse, SearchQuery, Paper, Citation, Cluster, Suggestion, AutoCompleteResponse

from models import elastic_models

from services.elastic_service import ElasticService
from services.elasticsearch_adapters import PaperAdapter, CitationAdapter, ClusterAdapter

from utils.helpers import getKeyOrDefault

router = APIRouter()
elastic_service = ElasticService()
paper_adapter = PaperAdapter(elastic_service)
cluster_adapter = ClusterAdapter(elastic_service)
citation_adapter = CitationAdapter(elastic_service)


@router.post('/search', response_model=SearchQueryResponse)
def perform_search(searchQuery: SearchQuery):
    docs_response = paper_adapter.search_papers(searchQuery)
    result_list = []
    for doc_hit in docs_response['hits']['hits']:
        result_list.append(build_paper_entity(_id=doc_hit['_id'], doc=doc_hit['_source']))
    total_results = docs_response['hits']['total']['value']
    return SearchQueryResponse(query_id=str(uuid4()), total_results=total_results, response=result_list)


@router.get('/paper/{id}')
def paper_info(id: str):
    docs_response = paper_adapter.get_paper_info(id)
    paper_entity_response = build_paper_entity(id, docs_response['hits']['hits'][0]['_source'])
    return PaperDetailResponse(query_id=str(uuid4()), paper=paper_entity_response)


@router.get('/citations/{id}')
def citations(id: str, page: int = 1, pageSize: int = 10):
    es_citations_response = citation_adapter.get_citations_for_paper(id, page, pageSize)
    result_list = []
    for doc_hit in es_citations_response['hits']['hits']:
        result_list.append(build_citation_entity(_id=doc_hit['_id'], doc=doc_hit['_source']))
    total_results = es_citations_response['hits']['total']['value']
    return CitationsResponse(query_id=str(uuid4()), total_results=total_results, citations=result_list)


@router.get('/cluster/{cid}')
def show_cluster_detail(cid: str):
    cluster_detail_response = cluster_adapter.get_cluster_info(cid)
    return ClusterDetailResponse(query_id=str(uuid4()),
                                 cluster=build_cluster_entity(cluster_detail_response['_source']))


@router.get('/showCiting/{cid}')
def show_citing(cid: str, sort: str, page: int, pageSize: int):
    cluster = elastic_models.Cluster.get(id=cid, using=elastic_service.get_connection())
    primary_cluster_detail = build_cluster_entity(id=cid, doc=cluster.to_dict(skip_empty=False))
    clusters = elastic_models.Cluster.mget(using=elastic_service.get_connection(), docs=cluster.cited_by)
    papers_list = []
    for each_cluster in clusters:
        if each_cluster.papers is not None:
            papers_list.extend(each_cluster.papers)
    papers_response = paper_adapter.get_sorted_papers(papers_list=papers_list, page=page, pageSize=pageSize, sort=sort)
    result_list = []
    for each_paper_hit in papers_response['hits']['hits']:
        print(each_paper_hit['_source'].to_dict().keys())
        result_list.append(build_paper_entity(_id=each_paper_hit['_id'], doc=each_paper_hit['_source']))
    total_results = papers_response['hits']['total']['value']
    return showCitingClustersResponse(query_id=str(uuid4()), total_results=total_results,
                                      cluster=primary_cluster_detail, papers=result_list)


@router.get('/suggest')
def get_suggestions(query: str):
    s = elastic_models.Paper.search(using=ElasticService().get_connection())
    s = s.suggest('auto_complete', query, completion={'field': 'title_suggest'})
    response = s.execute()
    suggestions = []
    for option in response.suggest.auto_complete[0].options:
        suggestions.append(Suggestion(type="paper", text=option._source.title, id=option._id))
    return AutoCompleteResponse(query_id=str(uuid4()), query=query, suggestions=suggestions)


@router.get('/similar/{id}')
def similar_papers(id: str):
    res = elastic_service.more_like_this_search("papers_next", id)
    result_list = []
    #print(res['hits']['hits'])
    f = False
    for doc in res['hits']['hits']:
        if not f:
            f = True
            for key in doc['_source']:
                print('key:')
                print(key)
                if key != 'abstract' and  key != 'text':
                    print(doc['_source'][key])
                print()
        result_list.append(build_similar_papers_entity(_id=doc['_id'], doc=doc['_source']))
    total_results = res['hits']['total']['value']
    return SimilarPapersResponse(query_id=str(uuid4()), total_results=total_results, similar_papers=result_list)


def build_paper_entity(_id, doc):
    return Paper(id=_id,
                 title=getKeyOrDefault(doc, 'title'),
                 venue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'title'),
                 year=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'year'),
                 n_cited_by=getKeyOrDefault(doc, 'ncites', default=0),
                 n_self_cites=getKeyOrDefault(doc, 'selfCites', default=0),
                 abstract=getKeyOrDefault(doc, 'abstract'),
                 bibtex="test_bibtex",
                 authors=get_authors_in_list(doc, 'authors'),
                 journal=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
                 publish_time=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'date'),
                 source="")


def get_authors_in_list(doc, field) -> List[str]:
    return [getKeyOrDefault(field, 'forename', default="") + " " + getKeyOrDefault(field, 'surname', default="") for
            field in getKeyOrDefault(doc, field, default={})]

def build_citation_entity(_id, doc):
    return Citation(id=_id,
                    cluster=getKeyOrDefault(doc, 'cluster_id'),
                    authors=get_authors_in_list(doc, 'authors'),
                    title=getKeyOrDefault(doc, 'title'),
                    venue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'title'),
                    venue_type=getKeyOrDefault(doc, 'venueType'),
                    year=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'year'),
                    pages=getKeyOrDefault(doc, 'pages'),
                    editors=getKeyOrDefault(doc, 'editors'),
                    publisher=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
                    pub_address=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'pub_address'),
                    volume=getKeyOrDefault(doc, 'volume'),
                    number=getKeyOrDefault(doc, 'number'),
                    tech=getKeyOrDefault(doc, 'tech'),
                    raw=getKeyOrDefault(doc, 'raw'),
                    paper_id=getKeyOrDefault(doc, 'paper_id'),
                    self=getKeyOrDefault(doc, 'self'))


def build_similar_papers_entity(_id, doc):
    return Citation(id=_id,
                    cluster=getKeyOrDefault(doc, 'cluster_id'),
                    authors=get_authors_in_list(doc, 'authors'),
                    title=getKeyOrDefault(doc, 'title'),
                    venue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'title'),
                    venue_type=getKeyOrDefault(doc, 'venueType'),
                    year=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'year'),
                    pages=getKeyOrDefault(doc, 'pages'),
                    editors=getKeyOrDefault(doc, 'editors'),
                    publisher=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
                    pub_address=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'pub_address'),
                    volume=getKeyOrDefault(doc, 'volume'),
                    number=getKeyOrDefault(doc, 'number'),
                    tech=getKeyOrDefault(doc, 'tech'),
                    raw=getKeyOrDefault(doc, 'raw'),
                    paper_id=getKeyOrDefault(doc, 'paper_id'),
                    self=getKeyOrDefault(doc, 'self'))


def build_cluster_entity(id, doc):
    return Cluster(cluster_id=id,
                   incollection=getKeyOrDefault(doc, 'in_collection', default=0),
                   cpublisher=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
                   cyear=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'date', default=0),
                   observations=getKeyOrDefault(doc, 'observations'),
                   selfCites=getKeyOrDefault(doc, 'selfCites'),
                   ctitle=getKeyOrDefault(doc, 'title'),
                   ctech=getKeyOrDefault(doc, 'ctech'),
                   cvol=getKeyOrDefault(doc, 'cvol'),
                   cvenue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'pub_place'),
                   cnum=getKeyOrDefault(doc, 'cnum'),
                   cpages=getKeyOrDefault(doc, 'cpages'),
                   cventype=getKeyOrDefault(doc, 'cventype'))
