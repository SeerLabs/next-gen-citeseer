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

    searchPaper(context, { queryString, page, pageSize, includeWithoutPdfs }) {
        return this.$axios
            .$post('/search', {
                queryString,
                page,
                pageSize,
                must_have_pdf: includeWithoutPdfs
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
