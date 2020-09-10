
import CoreApi from './CoreApi'

export default {
  getShowCiting (id, page, pageSize, sortBy) {
    return CoreApi().get('/showCiting/' + id, { params: { page, pageSize, sort: sortBy } })
  }
}
