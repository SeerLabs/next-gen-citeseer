import CoreApi from './CoreApi'

export default {
    searchPaper (queryString, page, pageSize) {
        return CoreApi().post('/search', {
            queryString: queryString,
            page: page,
            pageSize: pageSize
        })
        .then(function (response) {
            return response;
        })
        .catch(function (error) {
            console.log(error);
        });
    }
}
