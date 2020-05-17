<template>
  <b-container class="document-results-container">
    <ul>
      <li v-for="item in orderedDocuments" :key="item.id"> 
        <document-results-item class="document-results-item"
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
    import _ from 'lodash';

    export default {
        name: "DocumentResultsContainer",
        components: {
          DocumentResultsItem
        },
        props: {
          documents: Array,
          sortByKey: String
        },
        computed: {
          orderedDocuments: function() {
            return _.orderBy(this.documents, this.sortByKey, 'desc');
          }
        }
    }

</script>

<style scoped>
  .document-results-container {
    margin: 1.5em 0 1em 0;
    padding: 0;
  }

  .document-results-container ul {
    list-style: none;
    padding-left: 0;
  }

  .document-results-item {
    margin: .5em 0;
  }
  
</style>
