export default {
    getPaperWithPaperId ({context}, { pid }) {
      return this.$axios.$get('/paper', { params: {paper_id: pid}})
    },

    getPaperWithClusterId (context, { cid }){
      return this.$axios.$get('/paper', {params: {cluster_id: cid}})
    },

    getCitationsEntities (context, { id, page }) {
      return this.$axios.$get('/citations/' + id, { params: { page, pageSize: 10 } })
    },

    getSimilarPaper (context, { id, algo }) {
      return this.$axios.$get('/similar/' + id, { params: {algo}})
    },

    searchPaper(context, { queryString, page, pageSize, yearStart=null, yearEnd=null, author=null, publisher=null}) {

        if (yearStart === "0") {
            yearStart = null;
        }
        return this.$axios
            .$post('/search', {
                queryString,
                page,
                pageSize,
                yearStart,
                yearEnd,
                author,
                publisher
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error.response);
            });
    },

    getAggregations(context, { queryString }) {
        return this.$axios
                .$post('/aggregate', {
                    queryString
                })
                .catch(function(error) {
                    // eslint-disable-next-line
                    console.log(error.response);
                });    
    },

    searchAuthor(context, { queryString }) {
        return this.$axios
            .$post('/searchAuthor', {
                queryString
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error.response);
            });
    },

    getSuggestions(context, { queryString }) {
        return this.$axios
            .$get(`/suggest`, {params: { query: queryString}})
            .then(function(response) {
                return response;
            })
            .catch(function(error) {
                // eslint-disable-next-line
                console.log(error);
            });
    }, 

    getShowCiting (context, { id, page, pageSize, sortBy }) {
        return this.$axios.$get('/showCiting/' + id, { params: { page, pageSize, sort: sortBy } })
    }
}
