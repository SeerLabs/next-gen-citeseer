from models.api_models import SearchQuery
from services.elastic_service import ElasticService

class PaperAdapter:

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

class CitationAdapter:

    def __init__(self, elastic_service):
        self.elastic_service = ElasticService()

    def get_citations_for_paper(self, id, page, pageSize):
        return self.elastic_service.paginated_search('citations', id, page, pageSize, 'paperid')

class ClusterAdapter:

    def __init__(self, elastic_service):
        self.elastic_service = ElasticService()

    def get_clustered_papers(self, paper_id):
        """Given a paperID, return a few similar or clustered documents from the cluster index"""
        # Search the cluster index for a cluster which contains this specific paperID, return all other included papers
        return self.elastic_service.paginated_search('clusters', paper_id, 1, 10, 'included_papers', ['included_papers'])

    def get_cluster_info(self, cluster_id):
        return self.elastic_service.connection.get(index="clusters2", doc_type="cluster", id=cluster_id)

    def get_paper_ids_for_clusters(self, cid_list):
        return self.elastic_service.connection.mget(index="clusters2", doc_type="cluster", body={'ids': cid_list},
                                    _source_includes='included_papers')