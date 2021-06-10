import CoreApi from './CoreApi'

export default {
  getPaperWithPaperId (pid) {
    return CoreApi().get('/paper/', { params: {paper_id: pid}})
  },

  async getPaperswithPaperIds (pids) {
    return await CoreApi().post(`/mget_paper`, {"paper_id_list": pids})
            .then(function(response) {
                return response.data.response
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.error(error);
            })
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
