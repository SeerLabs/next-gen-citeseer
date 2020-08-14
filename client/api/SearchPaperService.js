import CoreApi from './CoreApi';

export default {
    searchPaper(queryString, page, pageSize, filters) {
        return CoreApi()
            .post('/search/papers', {
                queryString,
                page,
                pageSize,
                filters
            })
            .then(function(response) {
                return response;
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error);
            });
    },

    getAggregations(queryString) {
        return CoreApi()
            .post('/search/aggregations', {
                queryString
            })
            .then(function(response) {
                return response;
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error);
            });
    }
};
