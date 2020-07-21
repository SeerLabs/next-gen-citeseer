from services.elastic_service import ElasticService


class ClusterDao:

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
