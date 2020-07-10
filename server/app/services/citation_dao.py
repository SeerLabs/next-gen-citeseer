from services.elastic_service import ElasticService


class CitationDao:

    def __init__(self, elastic_service):
        self.elastic_service = ElasticService()

    def get_citations_for_paper(self, id, page, pageSize):
        return self.elastic_service.paginated_search('citations', id, page, pageSize, 'paperid')