import CoreApi from './CoreApi';

export default {
    searchPaper: function(queryString, page, pageSize) {
        return CoreApi()
            .post('/search', {
                queryString: queryString,
                page: page,
                pageSize: pageSize
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
