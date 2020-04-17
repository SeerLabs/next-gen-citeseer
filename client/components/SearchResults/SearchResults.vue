<template>
  <b-container>
    <b-row>
      <b-col cols="8">
        <search-results-list/>
      </b-col>
      <b-col cols="4">
        <search-results-filter/>
        <search-results-external-links/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
    import SearchResultsList from "../DocumentResults/DocumentResultsList.vue";
    import SearchResultsFilter from "./SearchResultsFilter.vue";
    import SearchResultsExternalLinks from "./SearchResultsExternalLinks";

    export default {
        name: "SearchResults",
        components: {
          SearchResultsList,
          SearchResultsFilter,
          SearchResultsExternalLinks
      }
    }
</script>

<style>

.search-result {
  margin-bottom: .5em;
}

</style>
