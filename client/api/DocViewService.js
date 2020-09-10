import CoreApi from './CoreApi'

export default {
  getPaperWithPaperId: function (pid) {
    return CoreApi().get('/paper/', { params: {paper_id: pid}})
  },
  getPaperWithClusterId: function (cid){
    return CoreApi().get('/paper/', {params: {cluster_id: cid}})
  },
  getCitationsEntities: function (id, page) {
    return CoreApi().get('/citations/' + id, { params: { page: page, pageSize: 10 } })
  },
  getSimilarPaper: function (id, algo) {
    return CoreApi().get('/similar/' + id, { params: {algo: algo}})
  }
}
