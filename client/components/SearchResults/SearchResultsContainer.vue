<template>
  <b-container class="search-result-container">
    <SearchResultsItem/>
    <SearchResultsItem/>
    <SearchResultsItem/>
  </b-container>
</template>

<script>
    import SearchResultsItem from "./SearchResultsItem";
    export default {
        name: "SearchResultsContainer",
        components: {
          SearchResultsItem
      }
    }

</script>

<style scoped>
  .search-result-container {
    margin: 1.5em 0 1em 0;
    padding: 0;
  }
</style>
