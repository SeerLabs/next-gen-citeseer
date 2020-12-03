import time
from multiprocessing import Pool
from pathlib import Path

from ingestion.csx_clusterer import KeyMatcherClusterer
from ingestion.csx_extractor import CSXExtractorImpl
from ingestion.interfaces import CSXIngester
from models.elastic_models import Cluster, KeyMap
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
        start_time = time.time()
        self.extractor.batch_extract_textual_data(dirpath)
        all_files = list(Path(dirpath).rglob("*.[tT][eE][iI]"))
        for filepath in all_files:
            count = count + 1
            if count % 20 == 0:
                print(count)
                print("--- %s seconds ---" % (time.time() - start_time))
            papers = self.extractor.extract_textual_data(filepath=str(filepath))
            self.clusterer.cluster_papers(papers)
        print("--- %s seconds ---" % (time.time() - start_time))


    def docs_generator(self, dirPath=None):
        count = 0
        all_files = list(Path(dirPath).rglob("*.[tT][eE][iI]"))
        for filepath in all_files:
            count = count + 1
            if count % 20 == 0:
                print(count)
            paper, citations = self.extractor.extract_textual_data(str(filepath))
            yield paper.to_dict(True)
            for citation in citations:
                yield citation.to_dict(True)


def parallel_ingest(eachfile):
    papers = CSXExtractorImpl().extract_textual_data(filepath=str(eachfile))
    KeyMatcherClusterer().cluster_papers(papers)


if __name__ == "__main__":
    csx_ingester = CSXIngesterImpl()
    Cluster.init(using=csx_ingester.elastic_service.get_connection())
    KeyMap.init(using=csx_ingester.elastic_service.get_connection())
    start_time = time.time()
    pool = Pool()
    pool.map(parallel_ingest, iter(Path("/data/ACL_results/2020100900").rglob("*.[tT][eE][iI]")))
    pool.close()
    pool.join()
    print("--- %s seconds ---" % (time.time() - start_time))
