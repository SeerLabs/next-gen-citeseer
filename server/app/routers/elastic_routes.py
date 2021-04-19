from typing import List, Optional
from uuid import uuid4

from elasticsearch_dsl import UpdateByQuery
from fastapi import APIRouter

import settings
from models.api_models import SearchQueryResponse, PaperDetailResponse, CitationsResponse, ClusterDetailResponse, \
    showCitingClustersResponse, SimilarPapersResponse, SearchQuery, Paper, Citation, Cluster, Suggestion, \
    AutoCompleteResponse

from models import elastic_models

from services.elastic_service import ElasticService

from utils.helpers import getKeyOrDefault

router = APIRouter()
elastic_service = ElasticService()


@router.post('/search', response_model=SearchQueryResponse)
def perform_search(searchQuery: SearchQuery):
    s = elastic_models.Cluster.search(using=elastic_service.get_connection())
    start = (searchQuery.page - 1) * searchQuery.pageSize
    if searchQuery.must_have_pdf:
        s = s.filter('term', has_pdf=True)
    s = s.query('multi_match', query=searchQuery.queryString, fields=['title', 'text'])
    s = s[start:start + searchQuery.pageSize]
    response = s.execute()
    result_list = []
    for doc_hit in response['hits']['hits']:
        result_list.append(build_paper_entity(cluster_id=doc_hit['_id'], doc=doc_hit['_source']))
    total_results = response['hits']['total']['value']
    return SearchQueryResponse(query_id=str(uuid4()), total_results=total_results, response=result_list)


@router.get('/paper')
def paper_info(paper_id: Optional[str] = None, cluster_id: Optional[str] = None):
    # if Called with cluster ID
    if cluster_id is not None:
        cluster = elastic_models.Cluster.get(id=cluster_id, using=elastic_service.get_connection())
        print(cluster.to_dict())
        paper_entity_response = build_paper_entity(cluster_id=cluster_id,
                                                   doc=cluster.to_dict())
        return PaperDetailResponse(query_id=str(uuid4()), paper=paper_entity_response)

    # if called with paper ID (SHA1)
    s = elastic_models.Cluster.search(using=elastic_service.get_connection())
    s = s.filter("term", paper_id=paper_id)
    response = s.execute()
    paper_entity_response = build_paper_entity(cluster_id=response['hits']['hits'][0]['_id'],
                                               doc=response['hits']['hits'][0]['_source'])
    return PaperDetailResponse(query_id=str(uuid4()), paper=paper_entity_response)


@router.get('/citations/{id}')
def citations(id: str, page: int = 1, pageSize: int = 10):
    s = elastic_models.Cluster.search(using=elastic_service.get_connection())
    start = (page - 1) * pageSize
    s = s.filter('term', cited_by=id)
    s = s[start:start + pageSize]
    response = s.execute()
    result_list = []
    for doc_hit in response['hits']['hits']:
        result_list.append(build_citation_entity(_id=doc_hit['_id'],
                                                 doc=doc_hit['_source']))
    total_results = response['hits']['total']['value']
    return CitationsResponse(query_id=str(uuid4()), total_results=total_results, citations=result_list)


@router.get('/showCiting/{cid}')
def show_citing_papers(cid: str, sort: str, page: int, pageSize: int):
    cluster = elastic_models.Cluster.get(id=cid, using=elastic_service.get_connection())
    primary_cluster_detail = build_cluster_entity(id=cid, doc=cluster.to_dict(skip_empty=False))
    papers_that_cite = []
    result_list = []
    total_results = 0
    for paper in cluster.cited_by:
        papers_that_cite.append(paper)
    if len(papers_that_cite) > 0:
        search = elastic_models.Cluster.search(using=elastic_service.connection) \
            .sort(_get_sort_param(sort)) \
            .filter('terms', paper_id=papers_that_cite, has_pdf=True)
        start = (page - 1) * pageSize
        search = search[start:start + pageSize]
        response = search.execute()
        for doc_hit in response['hits']['hits']:
            result_list.append(build_paper_entity(cluster_id=doc_hit['_id'], doc=doc_hit['_source']))
        total_results = response['hits']['total']['value']
    return showCitingClustersResponse(query_id=str(uuid4()), total_results=total_results,
                                      cluster=primary_cluster_detail, papers=result_list)


def _get_sort_param(param: str) -> dict:
    if param == "yearAsc":
        return {"pub_info.year": {'order': "asc", "nested": {"path": "pub_info"}}}
    elif param == "yearDesc":
        return {"pub_info.year": {'order': "desc", "nested": {"path": "pub_info"}}}
    elif param == "citCount":
        return {"_script": {"type": "number",
                            "script": {
                                "lang": "painless",
                                "source": "doc.cited_by.length"},
                            "order": "desc"}}
    else:
        # default sort by year desc
        return {"pub_info.year": {'order': "desc", "nested": {"path": "pub_info"}}}


@router.get('/suggest')
def get_suggestions(query: str):
    s = elastic_models.Cluster.search(using=ElasticService().get_connection())
    s = s.suggest('auto_complete', query, completion={'field': 'title_suggest'})
    response = s.execute()
    suggestions = []
    for option in response.suggest.auto_complete[0].options:
        suggestions.append(Suggestion(type="paper", text=option._source.title, id=option._id))
    return AutoCompleteResponse(query_id=str(uuid4()), query=query, suggestions=suggestions)


@router.get('/similar/{id}')
def similar_papers(id: str, algo: str):
    res = None
    if algo == 'Co-Citation':
        s = elastic_models.Cluster.search(using=elastic_service.get_connection(), index='clusters_next').filter('match',
                                                                                                                cited_by=id)
        res = s.execute()
    elif algo == 'Active Bibliography':
        s = elastic_models.Cluster.search(using=elastic_service.get_connection(), index='clusters_next').filter('match',
                                                                                                                cited_by=id)
        res = s.execute()
    else:
        res = elastic_service.more_like_this_search("papers_next", id)

    result_list = []
    for doc in res['hits']['hits']:
        result_list.append(build_similar_papers_entity(_id=doc['_id'], doc=doc['_source']))
    total_results = res['hits']['total']['value']
    return SimilarPapersResponse(query_id=str(uuid4()), total_results=total_results, similar_papers=result_list)


@router.delete('/delete/{id}')
def delete_paper(id: str):
    # Delete citations for paper
    ubq = UpdateByQuery(index=settings.CLUSTERS_INDEX).using(elastic_service.get_connection()) \
        .filter("term", cited_by=id).script(source="""
            for (int i=ctx._source.cited_by.length-1; i>=0; i--) {
                if (ctx._source.cited_by[i] == params.paper_to_remove) {
                    ctx._source.cited_by.remove(i);
                }
            }""", params={"paper_to_remove": id})

    response = ubq.execute()
    print(response.to_dict())

    # Delete Cluster for paper
    search_cluster = elastic_models.Cluster.search(index=settings.CLUSTERS_INDEX,
                                                   using=elastic_service.get_connection())
    search_cluster = search_cluster.filter('term', paper_id=id)
    response = search_cluster.execute()
    cluster_id = response['hits']['hits'][0]['_id']
    search_cluster.delete()

    # Delete KeyMaps
    search_keymap = elastic_models.KeyMap.search(using=elastic_service.get_connection())
    search_keymap = search_keymap.query('match', paper_id=cluster_id)
    search_keymap.delete()

    # Create an Audit entry
    new_user_request = elastic_models.UserRequest()
    new_user_request.request_type = "DELETE"
    new_user_request.status = "DONE"
    new_user_request.paper_id = id
    new_user_request.save(using=elastic_service.get_connection())


@router.delete('/unlist/{id}')
def unlist_paper(id: str):
    # Get Cluster for paper
    search_cluster = elastic_models.Cluster.search(using=elastic_service.get_connection())
    search_cluster = search_cluster.filter('term', paper_id=id)
    response = search_cluster.execute()
    cluster_id = response['hits']['hits'][0]['_id']

    # Make PDF availability as False
    cluster = elastic_models.Cluster.get(id=cluster_id, using=elastic_service.get_connection())
    cluster.has_pdf = False
    cluster.save(using=elastic_service.get_connection())

    # Create an Audit entry
    new_user_request = elastic_models.UserRequest()
    new_user_request.request_type = "UNLIST"
    new_user_request.paper_id = id
    new_user_request.status = "DONE"
    new_user_request.save(using=elastic_service.get_connection())


@router.post('/edit')
def user_request_correction(paper_id: str):
    # TODO: meta data correction; save edit in UserRequest index and later process in batch
    pass


def build_paper_entity(cluster_id, doc):
    paper_id = getKeyOrDefault(doc, 'paper_id', [''])[0]
    return Paper(id=paper_id,
                 title=getKeyOrDefault(doc, 'title'),
                 venue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'title'),
                 year=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'year'),
                 n_cited_by=len(getKeyOrDefault(doc, 'cited_by', default=[])),
                 n_self_cites=getKeyOrDefault(doc, 'selfCites', default=0),
                 abstract=getKeyOrDefault(doc, 'abstract'),
                 bibtex="test_bibtex",
                 authors=get_authors_in_list(doc, 'authors'),
                 journal=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
                 publish_time=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'date'),
                 source="",
                 cluster_id=cluster_id)


def get_authors_in_list(doc, field) -> List[str]:
    return [getKeyOrDefault(field, 'forename', default="") + " " + getKeyOrDefault(field, 'surname', default="") for
            field in getKeyOrDefault(doc, field, default={})]


def build_citation_entity(_id, doc):
    return Citation(id=_id,
                    cluster=_id,
                    in_collection=getKeyOrDefault(doc, 'has_pdf', default=False),
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
                    paper_id=getKeyOrDefault(doc, 'paper_id', default=[""])[0],
                    self=getKeyOrDefault(doc, 'self'))


def build_similar_papers_entity(_id, doc):
    return Citation(id=_id,
                    cluster=getKeyOrDefault(doc, 'paper_id') or _id,
                    in_collection=get_in_collection_as_int(doc),
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


def get_in_collection_as_int(doc):
    if getKeyOrDefault(doc, 'in_collection', False):
        return 1
    else:
        return 0


def build_cluster_entity(id, doc):
    return Cluster(cluster_id=id,
                   incollection=getKeyOrDefault(doc, 'in_collection', default=0),
                   cpublisher=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
                   cyear=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'year', default=0),
                   observations=getKeyOrDefault(doc, 'observations'),
                   selfCites=getKeyOrDefault(doc, 'selfCites'),
                   ctitle=getKeyOrDefault(doc, 'title'),
                   ctech=getKeyOrDefault(doc, 'ctech'),
                   cvol=getKeyOrDefault(doc, 'cvol'),
                   cvenue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'pub_place'),
                   cnum=getKeyOrDefault(doc, 'cnum'),
                   cpages=getKeyOrDefault(doc, 'cpages'),
                   cventype=getKeyOrDefault(doc, 'cventype'))
