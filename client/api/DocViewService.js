import CoreApi from './CoreApi'

export default {
  getPaperWithPaperId (pid) {
    return CoreApi().get('/paper/', { params: {paper_id: pid}})
  },
  getPaperWithClusterId (cid){
    return CoreApi().get('/paper/', {params: {cluster_id: cid}})
  },
  getCitationsEntities (id, page) {
    return CoreApi().get('/citations/' + id, { params: { page, pageSize: 10 } })
  }
}
