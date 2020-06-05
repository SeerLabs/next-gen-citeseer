<template>
    <b-row>
      <b-col md="8" id="search-results-list">
        <document-results-list :documents="documents" :totalPageResults="totalPageResults"/>
      </b-col>
      <b-col md="4" id="search-results-cards">
        <search-results-filter/>
        <search-results-external-links/>
      </b-col>
    </b-row>
</template>

<script>
    import DocumentResultsList from "../DocumentResults/DocumentResultsList.vue";
    import SearchResultsFilter from "./SearchResultsFilter.vue";
    import SearchResultsExternalLinks from "./SearchResultsExternalLinks";
    import searchPaperService from "~/api/SearchPaperService";

    export default {
        name: "SearchResults",
        components: {
          DocumentResultsList,
          SearchResultsFilter,
          SearchResultsExternalLinks
        },
        data() {
          return {
            queryString: '',
            documents: [],
            totalPageResults: 1000,
            pageSize: 10,
            page: 1
          }
        },
        methods: {
          searchQuery() {
            this.queryString = "test";
            searchPaperService.searchPaper(this.queryString, this.page, this.pageSize)
            .then(response => {
              console.log("RESPONSE: " + response.data);

              const results = [];
              for(var i in response.data.response) {
                results.push(response.data.response[i]);
              }
              this.documents = results;
              console.log(this.documents);
            });
          }
        },
        mounted: function() {
          this.searchQuery();
        }
    }
</script>

<style>

.search-result {
  margin-bottom: .5em;
}

#search-results-list {
  margin-bottom: 1em;
}
</style>
