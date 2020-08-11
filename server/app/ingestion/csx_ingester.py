from pathlib import Path

from ingestion.csx_clusterer import KeyMatcherClusterer
from ingestion.csx_extractor import CSXExtractorImpl
from ingestion.interfaces import CSXIngester
from models.elastic_models import Cluster, Author, Citation, Paper, PubInfo
from services.elastic_service import ElasticService


class CSXIngesterImpl(CSXIngester):
    def __init__(self):
        self.extractor = CSXExtractorImpl()
        self.clusterer = KeyMatcherClusterer()
        self.elastic_service = ElasticService()

    def ingest_paper(self, filepath):
        paper = self.extractor.extract_textual_data("../../test/resources/sample_tei.tei")
        self.clusterer.cluster_paper(paper)

    def batch_ingest(self, dirpath):
        count = 0
        self.extractor.batch_extract_textual_data(dirpath)
        all_files = list(Path(dirpath).rglob("*.[tT][eE][iI]"))
        for filepath in all_files:
            # print("processing file", filepath)
            count = count + 1
            if count % 20 == 0:
                print(count)
            paper = self.extractor.extract_textual_data(str(filepath))
            paper.paper_id = str(filepath).split('/')[4]
            self.clusterer.cluster_paper(paper)


if __name__ == "__main__":
    csx_ingester = CSXIngesterImpl()
    # Cluster.init(using=csx_ingester.elastic_service.get_connection())
    # Paper.init(using=csx_ingester.elastic_service.get_connection())
    # Author.init(using=csx_ingester.elastic_service.get_connection())
    # PubInfo.init(using=csx_ingester.elastic_service.get_connection())
    # Citation.init(using=csx_ingester.elastic_service.get_connection())
    # csx_ingester.ingest_paper("../../test/resources/sample_tei.tei")
    csx_ingester.batch_ingest("/data/ACL_results/2020072500/")
