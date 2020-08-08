from typing import List
from elasticsearch_dsl import Q, Nested, MultiSearch, Search
from models.api_models import SearchQuery
from models.elastic_models import Paper, Citation, Cluster, Author, PubInfo
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
            sort = 'year'
        elif sort == "yearDsc":
            sort = '-year'
        elif sort == "citCount":
            sort = '-ncites'
        else:
            sort = '-ncites'
        return self.elastic_service.paginated_search_with_ids(index="citeseerx", ids=papers_list,
                                                              page=page, pageSize=pageSize, sort=sort)


class CitationAdapter:

    def __init__(self, elastic_service):
        self.elastic_service = ElasticService()

    def get_citations_for_paper(self, id, page, pageSize):
        return self.elastic_service.paginated_search('citations', id, page, pageSize, 'paperid')


class ClusterAdapter:

    def __init__(self, elastic_service):
        self.elastic_service = elastic_service

    def get_clustered_papers(self, paper_id):
        """Given a paperID, return a few similar or clustered documents from the cluster index"""
        # Search the cluster index for a cluster which contains this specific paperID, return all other included papers
        return self.elastic_service.paginated_search('clusters', paper_id, 1, 10, 'included_papers',
                                                     ['included_papers'])

    def get_cluster_info(self, cluster_id):
        return self.elastic_service.connection.get(index="clusters2", doc_type="cluster", id=cluster_id)

    def get_paper_ids_for_clusters(self, cid_list):
        return self.elastic_service.connection.mget(index="clusters2", doc_type="cluster", body={'ids': cid_list},
                                                    _source_includes='included_papers')

    def cluster_paper(self, keys: List[str], paper: Paper):
        """
        Given a paper, checks if can belong to an existing cluster, else gets the new cluster
        :param keys: keys extracted from paper
        :param paper: paper to do cluster
        :return cluster_id: final cluster id, can be existing one or newly created
        """
        search = Cluster.search().params(request_timeout=100)
        first_key = self._get_first_key(keys)
        if first_key is None:
            return self._create_new_cluster_for_paper(paper, keys)
        query = Q("multi_match", query=first_key, fields=['keys'])
        response = search.using(client=self.elastic_service.get_connection()).query(query).execute()
        if any(response) is False:
            return self._create_new_cluster_for_paper(paper, keys)

        # case when existing cluster is found for the key, update it and return the id
        existing_cluster_id = response[0].meta.id
        # print(paper.to_dict())
        paper.save(using=self.elastic_service.get_connection())
        self._update_cluster_for_paper(cluster_id=existing_cluster_id, paper=paper, keys=keys)
        return existing_cluster_id

    def _update_cluster_for_paper(self, cluster_id: str, paper: Paper, keys: List[str]):
        cluster = Cluster.get(id=cluster_id, using=self.elastic_service.get_connection())
        self._add_keys_to_cluster(cluster, keys, self._get_first_key(keys))
        cluster.add_paper_id(paper.meta.id)
        cluster.save(using=self.elastic_service.get_connection())

    def _create_new_cluster_for_paper(self, paper: Paper, keys: List[str]):
        paper.save(using=self.elastic_service.get_connection())
        if len(keys) == 0:
            keys = ["$#@@$#@"]
        cluster = Cluster(
            title=paper.title,
            pub_info=Nested(PubInfo()).serialize(Nested(PubInfo()).deserialize(paper.pub_info)),
            in_collection=True,
            authors=Nested(Author()).serialize(Nested(Author()).deserialize(paper.authors)),
            keys=keys,
            papers=["$53#214*("],
            citations=["$53#214*("],
            cites=["$53#214*("],
            cited_by=["$53#214*("]
        )
        # Save cluster
        cluster.save(using=self.elastic_service.get_connection())
        self._update_cluster_for_paper(cluster_id=cluster.meta.id, paper=paper, keys=keys)
        return cluster.meta.id

    @classmethod
    def _get_first_key(cls, keys: List[str]):
        return keys[0] if len(keys) > 0 else None

    @classmethod
    def _add_keys_to_cluster(cls, cluster: Cluster, Keys: List[str], current_key: str):
        for key in Keys:
            if key != current_key:
                cluster.add_key(key)
        return

    def cluster_citation(self, keys: List[str], citation: Citation):
        """Given a paper, checks if can belong to an existing cluster, else gets the new cluster
            :param citation: the citation itself
            :param keys: keys extracted from citation
            :return cluster_id: final cluster id, can be existing one or newly created
        """
        ms = MultiSearch(index='clusters_next', using=self.elastic_service.get_connection())
        responses = []
        flag = 0
        for key in keys:
            if key is not None and key != "":
                ms = ms.add(Search(using=self.elastic_service.get_connection()).filter('term', keys=key))
                flag = 1
        if flag != 0:
            responses = ms.execute()
        matched_cluster_ids = []
        for response in responses:
            for hit in response:
                matched_cluster_ids.append(hit.meta.id)
        if len(matched_cluster_ids) == 0:
            return self._create_new_cluster_for_citation(citation, keys)
        elif len(matched_cluster_ids) >= 1:
            citation.cluster_id = matched_cluster_ids[0]
            print("existing cluster")
            print(citation.cluster_id)
            self._update_cluster_for_citation(matched_cluster_ids[0], keys, citation)
            return matched_cluster_ids[0]

    def _update_cluster_for_citation(self, cluster_id: str, keys: List[str], citation: Citation):
        cluster = Cluster.get(id=cluster_id, using=self.elastic_service.get_connection())
        # keys_to_update = keys.remove()
        cluster.extend_keys(keys)
        citation.save(using=self.elastic_service.get_connection())
        cluster.add_citation_id(citation.meta.id)
        cluster.save(using=self.elastic_service.get_connection())

    def _create_new_cluster_for_citation(self, citation: Citation, keys: List[str]):
        if len(keys) == 0:
            keys = ["$#@@$#@"]
        cluster = Cluster(
            title=citation.title,
            pub_info=Nested(PubInfo()).serialize(Nested(PubInfo()).deserialize(citation.pub_info)),
            in_collection=False,
            authors=Nested(Author()).serialize(Nested(Author()).deserialize(citation.authors)),
            keys=keys,
            cites=["$53#214*("],
            cited_by=["$53#214*("],
            papers=["$53#214*("],
            citations=["$53#214*("]
        )
        cluster.save(using=self.elastic_service.get_connection())
        self._update_cluster_for_citation(cluster.meta.id, keys, citation)
        return cluster.meta.id

    def relate_citing_clusters(self, citation_cluster_id: str, paper_cluster_id: str):
        if citation_cluster_id == paper_cluster_id:
            return
        citing_cluster = Cluster.get(id=paper_cluster_id, using=self.elastic_service.get_connection())
        cited_cluster = Cluster.get(id=citation_cluster_id, using=self.elastic_service.get_connection())
        citing_cluster.add_cites(cited_cluster)
        cited_cluster.add_cited_by(citing_cluster)
