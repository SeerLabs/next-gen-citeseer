import CoreApi from './CoreApi'

export default {
    searchPaper () {
        return CoreApi().get('/paper')
    }
}
