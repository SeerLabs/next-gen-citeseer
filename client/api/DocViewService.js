import CoreApi from './CoreApi'

export default {
  getPaperWithPaperId (pid) {
    return CoreApi().get('/paper/', { params: {paper_id: pid}})
  },

  async getPaperswithPaperIds (pids) {
    const papers = [];

    for (const pid of pids) {
        const paper = (await this.getPaperWithPaperId(pid)).data.paper;
        papers.push(paper);
    }
    
    return papers;
  },

  getPaperWithClusterId (cid){
    return CoreApi().get('/paper/', {params: {cluster_id: cid}})
  },
  getCitationsEntities (id, page) {
    return CoreApi().get('/citations/' + id, { params: { page, pageSize: 10 } })
  },
  getSimilarPaper (id, algo) {
    return CoreApi().get('/similar/' + id, { params: {algo}})
  }
}
