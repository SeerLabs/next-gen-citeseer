from zeep import Client

"""
This Service is to interact with old DOI Server for Legacy CiteSeerX
and won't be used for next gen seer
"""


class DOIService:
    def __init__(self):
        # TODO: create configurable endpoint.
        self.doi_wsdl_uri = (
            "http://csxdoi01.ist.psu.edu:8080/axis2/services/DOIServer?wsdl"
        )
        self.doi_client = Client(wsdl=self.doi_wsdl_uri)

    def get_doi(self, doiType: int):
        client = Client(wsdl=self.doi_wsdl_uri)
        return client.service.getDOI(doiType=doiType)


if __name__ == "__main__":
    doi_service = DOIService()
    new_doi = doi_service.get_doi(doiType=1)
    print(new_doi)
