import CoreApi from './CoreApi'
import TempApi from './TempApi'

export default {
    getPaperEntity (id) {
        return TempApi().get('/paper_entity', {params: {id: id}})
    },
    getCitationsEntities (id) {
        return CoreApi().get('/citation_entities',{params: {id: id}})
    },
    getDocPDF (doi) {
        return TempApi().get('/document', {params: {doi: doi}})
    }
    
}
