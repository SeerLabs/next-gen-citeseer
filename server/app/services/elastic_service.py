from elasticsearch import Elasticsearch
import requests
import json

class Elastic:

    def __init__(self):
        self.connection = Elasticsearch([{'host': '130.203.139.151', 'port': 9200}])


    def test_connection(self):
        req = requests.get('http://130.203.139.151:9200')
        content = req.content
        parsed = json.loads(content)
        self.print_response(parsed)

    def print_response(self, response):
        print(json.dumps(response, indent=4, sort_keys=True))

    '''
    input: index (str), the index that needs to be queried, usually citeseerx for papers or authors for authors
            q (str), the string query that is being made to Elastic
            source (list), the list of strings that represent the fields that must be included in the ES response
            fields_to_search (list), the list of strings that are going to searched for the query
    
    '''
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

    # Given a paperID, return all the relevant information for the paper
    def get_paper_info(self, paperID):
        #Search the citeseerx index for this specific paperID and return all fields associated with a hit
        return self.paginated_search('citeseerx', paperID, 1, 10, 'paper_id')

    # Given a paperID, return a few similar or clustered documents from the cluster index
    # There is a more simple way of thinking of this function, we could just use clusterID if we have it cached either in front end or backend for specific paper
    def get_clustered_papers(self, paperID):
        # Search the cluster index for a cluster which contains this specific paperID, return all other included papers
        return self.paginated_search('clusters', paperID, 1, 10, 'included_papers', ['included_papers'])

'''
ES = Elastic()
ES.test_connection()
#ES.refined_search('citeseerx', 'citeseer', ['title', 'text'])
paperID = "10.1.1.170.7725"

ES.get_paper_info(paperID)
ES.get_citations(paperID)
ES.get_clustered_papers(paperID)

'''