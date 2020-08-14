from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, MultiSearch, Q, A

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

    
    def get_aggregations(self, index, query, query_fields, aggs_fields, size=10, order={'_count': 'desc'}):
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

      if filters:
        if 'years' in filters:
          year_filter = Q('range', year={'gte': filters.years.start, 'lte': filters.years.end})
          query_filters.append(year_filter)

        if 'authors' in filters:
          author_filter = Q('terms', authors__name__keyword=filters.authors)
          query_filters.append(author_filter)

      s.query = Q('bool', must=[doc_search], filter=query_filters)
      s = s[start:pageSize]

      response = s.execute()

      self.print_response(response)
      return response


    def paginated_search_with_ids(self, index, page, pageSize, ids, sort, source=None):
      s = Search(index=index, using=self.connection)

      if source:
        s.source(includes=[source])
      print(ids)
      
      start = (page-1)*pageSize
      s = s.query('ids', values=ids)
      s = s.sort(sort)
      s = s[start:pageSize]
      
      response = s.execute()
      self.print_response(response)
      return response