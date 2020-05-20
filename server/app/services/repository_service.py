import requests
from pathlib import Path


class RepositoryService:
    def __init__(self):
        #TODO: create a service endpoint that can be configured.
        self.repository_endpoint = None

    def get_document(self, doi, file_type, repid):
        file_name = Path(doi)
        url = "http://csxrepo01.ist.psu.edu/document"
        payload = {'doi': doi, 'type': file_type, 'repid': repid, 'key': 'c1t3s33r'}
        response = requests.get(url, params=payload)
        return response
