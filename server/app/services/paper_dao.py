from models.api_models import SearchQuery
from services.elastic_service import ElasticService


class PaperDao:

    def __init__(self, elastic_service):
        self.elastic_service = ElasticService()

    def get_paper_info(self, paperID):
        """Search the citeseerx index for this specific paperID and return all fields associated with a hit
        Given a paperID, return all the relevant information for the paper"""
        return self.elastic_service.paginated_search('citeseerx', paperID, 1, 10, 'paper_id')

    def search_papers(self, searchQuery: SearchQuery):
        return self.elastic_service.paginated_search('citeseerx', searchQuery.queryString, searchQuery.page,
                                                     searchQuery.pageSize, ['title', 'text'])

    def get_sorted_papers(self, papers_list, page, pageSize, sort):
        """Given Paper IDs get them sorted in desired order with Pagination support"""
        if sort == "yearAsc":
            sort = 'year:asc'
        elif sort == "yearDsc":
            sort = 'year:desc'
        elif sort == "citCount":
            sort = 'ncites:desc'
        else:
            sort = 'ncites:desc'
        return self.elastic_service.paginated_search_with_ids(index="citeseerx", ids=papers_list,
                                                              page=page, pageSize=pageSize, sort=sort)
