<template>
  <b-container>
    <b-row>
      <b-col cols="8">
        <document-results-list :documents="documents" :totalPageResults="totalPageResults"/>
      </b-col>
      <b-col cols="4">
        <search-results-filter/>
        <search-results-external-links/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
    import DocumentResultsList from "../DocumentResults/DocumentResultsList.vue";
    import SearchResultsFilter from "./SearchResultsFilter.vue";
    import SearchResultsExternalLinks from "./SearchResultsExternalLinks";

    export default {
        name: "SearchResults",
        components: {
          DocumentResultsList,
          SearchResultsFilter,
          SearchResultsExternalLinks
        },
        data() {
          return {
            documents: [
              {'title': 'Document Title', 'type': 'DOCUMENT', 'authors': 'Abcdefg Lastname',
              'year': '2018', 'abstract': 'Lorem ipsum', 'numCitations': 20},
              {'title': 'ABCDEFG', 'type': 'DOCUMENT', 'authors': 'Hijklmno Pqrstuv',
              'year': '2020', 'abstract': 'Lorem ipsum', 'numCitations': 3},
              {'title': 'EFGHIJK', 'type': 'CITATION', 'authors': 'Firstname Lastname',
              'year': '2021', 'abstract': 'Lorem ipsum', 'numCitations': 30}
            ],
            totalPageResults: 1000
          }
        }  
    }
</script>

<style>

.search-result {
  margin-bottom: .5em;
}

</style>
