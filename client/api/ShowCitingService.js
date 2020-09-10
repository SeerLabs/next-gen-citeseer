
import CoreApi from './CoreApi'

export default {
  getShowCiting: function (id, page, pageSize, sortBy) {
    return CoreApi().get('/showCiting/' + id, { params: { page: page, pageSize: pageSize, sort: sortBy } })
  }
}
