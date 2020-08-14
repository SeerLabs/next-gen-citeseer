import CoreApi from './CoreApi';

export default {
    searchPaper(queryString, page, pageSize) {
        return CoreApi()
            .post('/search', {
                queryString,
                page,
                pageSize
            })
            .then(function(response) {
                return response;
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error.response.data);
            });
    }
};
