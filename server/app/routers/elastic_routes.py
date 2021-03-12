from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter

from models.api_models import SearchQueryResponse, PaperDetailResponse, CitationsResponse, ClusterDetailResponse, \
    showCitingClustersResponse, SimilarPapersResponse, SearchQuery, Paper, Citation, Cluster, Suggestion, \
    AutoCompleteResponse, PublicationInfo, Facets, SearchAuthorResponse

from models import elastic_models

from services.elastic_service import ElasticService

from utils.helpers import getKeyOrDefault
from elasticsearch_dsl import Q


router = APIRouter()
elastic_service = ElasticService()

@router.post('/search', response_model=SearchQueryResponse)
def perform_search(searchQuery: SearchQuery):
    s = elastic_models.Cluster.search(using=elastic_service.get_connection())
    start = (searchQuery.page - 1) * searchQuery.pageSize
    s = s.filter('term', has_pdf=True)

    if searchQuery.year is not None:
        yr_queries =[]
        for yr in searchQuery.year:
            q=Q("nested", path="pub_info", query=Q("term", **{'pub_info.year.keyword':yr}))
            yr_queries.append(q)
        s = s.query('bool',should=yr_queries)

    if searchQuery.publisher is not None:
        publisher_queries =[]
        for pub in searchQuery.publisher:
            q=Q("nested", path="pub_info", query=Q("term", **{'pub_info.publisher.keyword':pub}))
            publisher_queries.append(q)
        s = s.query('bool',should=publisher_queries)

    if searchQuery.author is not None:
        athr_queries =[]
        for athr in searchQuery.author:
            q=Q("nested", path="authors", query=Q("term", **{'authors.fullname.keyword':athr}))
            athr_queries.append(q)
        s = s.query('bool',should=athr_queries)

    s = s.query('multi_match', query=searchQuery.queryString, fields=['title', 'text'])

    s.aggs.bucket('all_pub_info1', 'nested', path='pub_info') \
        .metric('pub_info_year_count', 'cardinality', field='pub_info.year.keyword') \
        .bucket('pub_info_year_list', 'terms', field='pub_info.year.keyword')
    
    s.aggs.bucket('all_authors', 'nested', path='authors') \
        .metric('authors_count', 'cardinality', field='authors.fullname.keyword') \
        .bucket('authors_fullname_terms', 'terms', field='authors.fullname.keyword')

    s.aggs.bucket('all_pub_info2', 'nested', path='pub_info') \
        .metric('pub_info_publisher_count', 'cardinality', field='pub_info.publisher.keyword') \
        .bucket('pub_info_publisher_list', 'terms', field='pub_info.publisher.keyword')

    s = s[start:start + searchQuery.pageSize]
    response = s.execute()
    result_list = []
    for doc_hit in response['hits']['hits']:
        result_list.append(build_paper_entity(cluster_id=doc_hit['_id'], doc=doc_hit['_source']))
    total_results = response['hits']['total']['value']
    aggregations = {"agg": build_facets(response['aggregations']['all_pub_info1'],
                                response['aggregations']['all_pub_info2'],
                                response['aggregations']['all_authors'])}
    return SearchQueryResponse(query_id=str(uuid4()), total_results=total_results, response=result_list, aggregations=aggregations)

@router.get('/paper')
def paper_info(paper_id: Optional[str] = None, cluster_id: Optional[str] = None):
    if cluster_id is not None:
        cluster = elastic_models.Cluster.get(id=cluster_id, using=elastic_service.get_connection())
        paper_id = cluster.paper_id[0]
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
def show_citing(cid: str, sort: str, page: int, pageSize: int):
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
            .filter('terms', paper_id=papers_that_cite)
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
        return {"_script": {"type" : "number",
                            "script" : {
                                "lang": "painless",
                                "source": "doc.cited_by.length"},
                            "order" : "desc"}}
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


@router.post('/searchAuthor',response_model=SearchAuthorResponse)
def search_facet(searchQuery: str):
    s = elastic_models.Cluster.search(using=elastic_service.get_connection())
    s=s.query("nested", path="authors", query=Q('multi_match', query=searchQuery, fields=['authors.fullname']))
    response = s.execute()
    result_list = []
    for doc_hit in response['hits']['hits']:
        result_list.append(getKeyOrDefault(getKeyOrDefault(doc_hit['_source'], 'authors'), 'fullname'))
    total_results = response['hits']['total']['value']
    return SearchAuthorResponse(query_id=str(uuid4()),total_results=total_results,response=result_list)


def build_paper_entity(cluster_id, doc):
    return Paper(id=getKeyOrDefault(doc, 'paper_id')[0],
                 title=getKeyOrDefault(doc, 'title'),
                 venue=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'title'),
                 year=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'year'),
                 publisher=getKeyOrDefault(getKeyOrDefault(doc, 'pub_info'), 'publisher'),
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


def build_facets(agg_dict_yr,agg_dict_pub,agg_dict_athr):
    return Facets(pub_info_year_count= getKeyOrDefault(getKeyOrDefault(agg_dict_yr,'pub_info_year_count'),'value'),
                 pub_info_year_list= get_aggregation_list(
                     getKeyOrDefault(getKeyOrDefault(agg_dict_yr,'pub_info_year_list'),'buckets')),
                 pub_info_publisher_count= getKeyOrDefault(getKeyOrDefault(agg_dict_pub,'pub_info_publisher_count'),'value'),
                 pub_info_publisher_list= get_aggregation_list(
                     getKeyOrDefault(getKeyOrDefault(agg_dict_pub,'pub_info_publisher_list'),'buckets')),
                 authors_count= getKeyOrDefault(getKeyOrDefault(agg_dict_athr,'authors_count'),'value'),
                 authors_fullname_terms= get_aggregation_list(
                     getKeyOrDefault(getKeyOrDefault(agg_dict_athr,'authors_fullname_terms'),'buckets')))


def get_aggregation_list(bucket):
    agg_list = []
    for item in bucket:
        agg_list.append(PublicationInfo(key=item['key'], doc_count=item['doc_count']))
    return agg_list

