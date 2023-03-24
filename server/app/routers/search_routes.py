from fastapi import FastAPI, HTTPException, Request
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch_dsl import UpdateByQuery
from fastapi import APIRouter
from limiter import limiter
from fastapi.middleware.cors import CORSMiddleware
from models.api_models import (
    SearchQueryResponse,
    PaperDetailResponse,
    CitationsResponse,
    ClusterDetailResponse,
    showCitingClustersResponse,
    SimilarPapersResponse,
    SearchQuery,
    AggregationQuery,
    Paper,
    Citation,
    Cluster,
    Suggestion,
    AutoCompleteResponse,
    PublicationInfo,
    Facets,
    SearchAuthorResponse,
    SearchFilter,
    AggregationResponse,
    MGetRequest,
)

from models import elastic_models

from services.elastic_service import ElasticService

from utils.helpers import getKeyOrDefault
from elasticsearch_dsl import Q
import json

app = FastAPI()

router = APIRouter()
elastic_service = ElasticService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


rate_limit_string = "5/minute"


@router.post("/search", response_model=SearchQueryResponse)
# @limiter.limit(rate_limit_string)
def perform_search(request: Request, searchQuery: SearchQuery):
    s = elastic_models.Cluster.search(using=elastic_service.get_connection())

    start = (searchQuery.page - 1) * searchQuery.pageSize
    #s = s.filter("term", has_pdf=True)
    """
    if searchQuery.yearStart is not None and searchQuery.yearEnd is not None:
        q = Q("nested", path="pub_info", query=Q(
            "range", **{'pub_info.year.keyword': {'gte': searchQuery.yearStart, 'lte': searchQuery.yearEnd}}))
        s = s.query(q)

    if searchQuery.publisher is not None and len(searchQuery.publisher) > 0:
        publisher_queries = []
        for pub in searchQuery.publisher:
            q = Q("nested", path="pub_info", query=Q(
                "term", **{'pub_info.publisher.keyword': pub}))
            publisher_queries.append(q)
        s = s.query('bool', should=publisher_queries)

    if searchQuery.author is not None and len(searchQuery.author) > 0:
        athr_queries = []
        for athr in searchQuery.author:
            q = Q("nested", path="authors", query=Q(
                "term", **{'authors.fullname.keyword': athr}))
            athr_queries.append(q)
        s = s.query('bool', should=athr_queries)
    """
    if searchQuery.must_have_pdf:
        s = s.filter("term", has_pdf=True)

    # s = s.query('match', query=searchQuery.queryString,
    #           fields=['title', 'text'])
    q1 = Q("match", title=searchQuery.queryString)
    q2 = Q("match", text=searchQuery.queryString)
    q3 = Q("range", **{'pub_info.year': {'gte': searchQuery.yearStart, 'lte': searchQuery.yearEnd}})

    # If the year range in query is the default [1913, CurrentYear], then use general query. Else, that means range slider has been used to filter a specfic year range.
    if (searchQuery.yearStart == 1913 and searchQuery.yearEnd == date.today().year and searchQuery.must_have_pdf):
        q = Q("bool", must=q2, should=q1)
    elif (searchQuery.must_have_pdf):
        q = Q("bool", must=[q2, q3], should=q1)
    else:
        q = Q("bool", should=[q1, q2])

    s = s.query(q)
    print(s.to_dict())

    total_results = s.count()

    # Apply sorting
    if searchQuery.sortBy == "Citation":
        s = s.sort({"cited_by": {"order": "desc"}})
    elif searchQuery.sortBy == "Year":
        s = s.sort({"pub_info.year": {"order": "desc"}})
    s.aggs.bucket("all_pub_info1", "terms", field="pub_info.year").metric(
        "pub_info_year_count", "cardinality", field="pub_info.year"
    ).bucket("pub_info_year_list", "terms", field="pub_info.year")

    s.aggs.bucket("all_authors", "nested", path="authors").metric(
        "authors_count", "cardinality", field="authors.fullname.keyword"
    ).bucket("authors_fullname_terms", "terms", field="authors.fullname.keyword")

    s.aggs.bucket("all_pub_info2", "terms", field="pub_info.year").metric(
        "pub_info_publisher_count", "cardinality", field="pub_info.publisher.keyword"
    ).bucket("pub_info_publisher_list", "terms", field="pub_info.publisher.keyword")

    # Aggregate minimum year | response['aggregations']['pub_info']['min_year'] returns {'value': min_year}
    s.aggs.bucket("pub_info_path", "terms", field="pub_info.year").metric(
        "min_year", "min", field="pub_info.year"
    )

    s = s[start : start + searchQuery.pageSize]
    # print(str(s.to_dict()).replace("'", '"'))
    print(s.to_dict())
    response = s.execute()
    print(response.to_dict())
    result_list = []
    for doc_hit in response["hits"]["hits"]:
        result_list.append(
            build_paper_entity(cluster_id=doc_hit["_id"], doc=doc_hit["_source"])
        )
    aggregations = {
        "agg": build_facets(
            response["aggregations"]["all_pub_info1"],
            response["aggregations"]["all_pub_info2"],
            response["aggregations"]["all_authors"],
            response["aggregations"]["pub_info_path"],
        )
    }
    print(s.to_dict())
    return SearchQueryResponse(
        query_id=str(uuid4()),
        total_results=total_results,
        response=result_list,
        aggregations=aggregations,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
