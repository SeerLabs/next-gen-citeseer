<template>
  <b-container class="document-results-list">
    <ul>
      <li v-for="item in documents" :key="item.id"> 
        <document-results-item class="document-results-item"
          :doc_id="item.id"
          :title="item.title"
          :type="item.type" 
          :authors="item.authors"
          :year="item.year"
          :abstract="item.abstract"
          :numCitations="item.numCitations"
        />
      </li>
    </ul>
  </b-container>
</template>

<script>
    import DocumentResultsItem from "./DocumentResultsItem";

    export default {
        name: "DocumentResultsList",
        components: {
          DocumentResultsItem
        },
        props: {
          documents: Array,
        },
    }

</script>

<style scoped>
  .document-results-list {
    margin: 1.5em 0 1em 0;
    padding: 0;
  }

  .document-results-list ul {
    list-style: none;
    padding-left: 0;
  }

  .document-results-item {
    margin: .5em 0;
  }
  
</style>
