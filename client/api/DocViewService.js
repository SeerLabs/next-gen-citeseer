import CoreApi from './CoreApi'

export default {
  getPaperEntity (id) {
    return CoreApi().get('/paper/' + id)
  },
  getCitationsEntities (id, page) {
    return CoreApi().get('/citations/' + id, { params: { page, pageSize: 10 } })
  }
}
