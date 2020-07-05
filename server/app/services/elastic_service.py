from elasticsearch import Elasticsearch
import requests
import json


class ElasticService:

    def __init__(self):
        self.connection = Elasticsearch([{'host': '130.203.139.151', 'port': 9200}])

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

    # Given a paperID, return all the relevant information for the paper
    def get_paper_info(self, paperID):
        #Search the citeseerx index for this specific paperID and return all fields associated with a hit
        return self.paginated_search('citeseerx', paperID, 1, 10, 'paper_id')

    def get_clustered_papers(self, paper_id):
        """Given a paperID, return a few similar or clustered documents from the cluster index"""
        # Search the cluster index for a cluster which contains this specific paperID, return all other included papers
        return self.paginated_search('clusters', paper_id, 1, 10, 'included_papers', ['included_papers'])

    def get_cluster_info(self, cluster_id):
        return self.connection.get(index="clusters2", doc_type="cluster", id=cluster_id)

    def get_paper_ids_for_clusters(self, cid_list):
        return self.connection.mget(index="clusters2", doc_type="cluster", body={'ids': cid_list},
                                    _source_includes='included_papers')

    def get_sorted_papers(self, papers_list, page, pageSize, sort):
        if sort == "yearAsc":
            sort = 'year:asc'
        elif sort == "yearDsc":
            sort = 'year:desc'
        elif sort == "citCount":
            sort = 'ncites:desc'
        else:
            sort = 'ncites:desc'
        return self.paginated_search_with_ids(index="citeseerx", ids=papers_list,
                                              page=page, pageSize=pageSize, sort=sort)
