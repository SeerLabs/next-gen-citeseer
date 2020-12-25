from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, MultiSearch, Q, A
from elasticsearch_dsl.query import MoreLikeThis

import requests
import json

class ElasticService:

    def __init__(self):
        self.connection = Elasticsearch([{'host': '130.203.139.151', 'port': 9200}])

    def get_connection(self):
        return self.connection

    def test_connection(self):
        req = requests.get('http://130.203.139.151:9200')
        content = req.content
        parsed = json.loads(content)
        self.print_response(parsed)

    def print_response(self, response):
        # print(json.dumps(response.json(), indent=4, sort_keys=True))
        print(response['hits']['hits'])

    
    def get_aggregations(self, index, query, query_fields, size=10, order={'_count': 'desc'}):
        aggs_fields = [{'key': 'authors', 'field_name': 'authors.name.keyword'}]

        s = Search(index=index, using=self.connection)
        s.query = Q('multi_match', query=query, fields=query_fields)

        for item in aggs_fields:
          a = A('terms', field=item['field_name'], size=10, order={'_count': 'desc'})
          s.aggs.bucket(item['key'], a)

        s = s[0:0]

        return s.execute()['aggregations']


    def paginated_search(self, index, query, page, pageSize, fields_to_search, source=None, filters=None):
        s = Search(index=index, using=self.connection)

        if source:
          s.source(includes=[source])

        start = (page-1)*pageSize
        doc_search = Q('multi_match', query=query, fields=fields_to_search)
        
        query_filters = []

        if filters is not None:
          if filters.years:
            year_filter = Q('range', year={'gte': filters.years.start, 'lte': filters.years.end})
            query_filters.append(year_filter)

          if filters.authors:
            for author in filters.authors:
              query_filters.append(Q('term', authors__name__keyword=author))

        s.query = Q('bool', must=query_filters, filter=[doc_search])

        start = (page-1)*pageSize
        s = s[start : start+pageSize]

        response = s.execute()

        # self.print_response(response)
        return response


    def paginated_search_with_ids(self, index, page, pageSize, ids, sort, source=None):
        s = Search(index=index, using=self.connection)

        if source:
            s.source(includes=[source])

        start = (page - 1) * pageSize
        s = s.query('ids', values=ids)
        s = s.sort(sort)
        s = s[start:start + pageSize]

        return s.execute()


    def more_like_this_search(self, index, id):
        s = Search(index=index, using=self.connection)
        s = s.query(MoreLikeThis(like={'_id': id, '_index': index}, fields=["title", "abstract"], min_term_freq=3, min_word_length=6, max_query_terms=12))
        response = s.execute()
        return response
