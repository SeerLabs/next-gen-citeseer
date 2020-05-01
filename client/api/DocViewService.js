import CoreApi from './CoreApi'

export default {
    getPaperEntity (id) {
        return CoreApi().get('/paper_entity', {params: {id: id}})
    },
    getCitationsEntities (id) {
        return CoreApi().get('/citation_entities',{params: {id: id}})
    }
}
