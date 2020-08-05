from elasticsearch import Elasticsearch
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
        print(json.dumps(response, indent=4, sort_keys=True))

    def paginated_search(self, index, query, page, pageSize, fields_to_search, source=None):

        body = {
                "from": (page-1)*pageSize,
                "size": pageSize,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": fields_to_search
                    }
                }
        }

        if source:
            body["_source"] = source

        return self.connection.search(index=index, body=body)

    def paginated_search_with_ids(self, index, page, pageSize, ids, sort, source=None):

        body = {
                "from": (page-1)*pageSize,
                "size": pageSize,
                "query": {
                    "ids": {
                        "values": ids
                    }
                }
        }

        if source:
            body["_source"] = source

        return self.connection.search(index=index, body=body, sort=sort)
