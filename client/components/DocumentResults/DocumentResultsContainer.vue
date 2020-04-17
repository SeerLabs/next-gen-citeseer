<template>
  <b-container class="document-results-container">
    <DocumentResultsItem
      :title="document_title"
      :type="document_type",
      :authors="document_authors"
      :year="document_year"
      :abstract="document_abstract"
      :num-citations="document_num_citations"
    />
  </b-container>
</template>

<script>
    import DocumentResultsItem from "./DocumentResultsItem";
    export default {
        name: "DocumentResultsContainer",
        components: {
          DocumentResultsItem
        },

        data() {
          return {
            document_title: "Try your query at",
            document_type: "DOCUMENT",
            document_authors: "Firstname Lastname",
            document_year: "2020",
            document_abstract: "TEST",
            document_num_citations: 200
          }
        }
    }

</script>

<style scoped>
  .document-results-container {
    margin: 1.5em 0 1em 0;
    padding: 0;
  }
</style>
