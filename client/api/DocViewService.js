import CoreApi from './CoreApi'

export default {
    getPaperEntity (id) {
        return CoreApi().get('/paper/' + id)
    },
    getCitationsEntities (id) {
        return CoreApi().get('/citation_entities',{params: {id: id}})
    }
}
