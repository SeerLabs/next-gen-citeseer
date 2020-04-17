<template>
  <b-container class="search-result-list">
    <b-row class="search-results-header">
      <b-col sm="6">Results 1 - 10 of #####</b-col>
      <b-col sm="6">
        <div class="search-results-sorting">
          Sort by Relevance
        </div>
      </b-col>
    </b-row>

    <SearchResultsContainer/>

    <b-row class="search-results-pagination">
      <b-col sm="6">Page 1 of 2</b-col>
    </b-row>

  </b-container>
</template>

<script>
    import SearchResultsContainer from "./DocumentResultsContainer.vue";
    export default {
        name: "SearchResultsList",
        components: {
          SearchResultsContainer
      }
    }
</script>

<style scoped>
  .search-result-list {
    background-color: lightgrey;
    padding: .5em;
  }

  .search-results-sorting {
    text-align: right;
  }

</style>
