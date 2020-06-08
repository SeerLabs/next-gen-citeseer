<template>
  <b-container class="document-result-list">
    <b-row class="document-results-header">
      <b-col sm="6">Results {{(page-1)*pageSize + 1}} - {{(page-1)*pageSize + pageSize}} of {{totalPageResults}}</b-col>
      <b-col sm="6">
        <div class="document-results-sorting">
          Sort by
          <b-dropdown
            variant="primary"
            class="m-2 results-dropdown">

              <template v-slot:button-content>
                {{ sortByDisplay }}
              </template>
              
              <ul>
                <li v-for="(item, key) in sortDropdown" :key="key">
                    <b-dropdown-item
                    :name="key"
                    v-on:click="sortResults">
                      {{ item.displayName }}
                    </b-dropdown-item>
                </li>
              </ul>

          </b-dropdown>
        </div>
      </b-col>
    </b-row>

    <document-results-container :documents="documents" :sortByKey="sortByKey"/>
    
  </b-container>
</template>

<script>
    import Vue from 'vue';
    import DocumentResultsContainer from "./DocumentResultsContainer.vue";

    export default {
        name: "DocumentResultsList",
        components: {
          DocumentResultsContainer
        },
        props: {
          documents: Array,
          totalPageResults: Number,
          page: Number,
          sortDropdown: Object
        },
        data() {
          return {
            pageSize: 10,
            sortByDisplay: 'Relevance',
          }
        },
        computed: {
          currentPageLocation: function() {
            return this.pageSize * (this.currentPage-1) + 1;
          }
        },
        methods: {
          sortResults: function(event) {
            console.log(event);
            const dropdownItem = event.target.name;
            this.sortByDisplay = event.target.text;
            this.sortByKey = this.sortDropdown[dropdownItem].sortByKey;

            this.$emit('input', this.sortByDisplay);
          },
        }
    }
</script>

<style scoped>
  .document-result-list {
    background-color: lightgrey;
    padding: .5em;
  }

  .document-results-sorting {
    text-align: right;
  }

  .results-dropdown li {
    list-style: none;
  }

  .results-dropdown ul {
    padding: 0;
  }
</style>
