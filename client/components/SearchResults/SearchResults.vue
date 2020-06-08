<template>
    <div v-cloak>
      <b-row>
				<b-col sm="8" id="search-box-container">
					<search-box v-model="queryString" @submit="searchQuery" />
				</b-col>
			</b-row>

      <b-row>
        <b-col v-if="loadingState" md="8">
            <b-spinner class="spinner" label="Loading..."></b-spinner>
        </b-col>
        <b-col v-else md="8" id="search-results-list">
          <h3>{{sortBy}}</h3>
          <document-results-list 
            :documents="documents"
            :totalPageResults="totalPageResults"
            :page="page"
            :sortDropdown="sortDropdown"
            v-model="sortBy"
          />
          <b-pagination
            :total-rows="totalPageResults" 
            v-model="page"
            :per-page="pageSize"
            @input="searchQuery"
          />
        </b-col>
        <b-col md="4" id="search-results-cards">
          <search-results-filter/>
          <search-results-external-links/>
        </b-col>
      </b-row>
    </div>
</template>

<script>
    import DocumentResultsList from "../DocumentResults/DocumentResultsList.vue";
    import SearchResultsFilter from "./SearchResultsFilter.vue";
    import SearchResultsExternalLinks from "./SearchResultsExternalLinks";
    import SearchBox from '~/components/SearchBox.vue'
    import searchPaperService from "~/api/SearchPaperService";

    export default {
        name: "SearchResults",
        components: {
          DocumentResultsList,
          SearchResultsFilter,
          SearchResultsExternalLinks,
          SearchBox
        },
        data() {
          return {
            queryString: '',
            documents: [],
            totalPageResults: 0,
            pageSize: 10,
            page: 1,
            loadingState: false,
            sortBy: 'relevance',
            sortDropdown: {
              'sort-relevance': {'displayName': 'Relevance', 'sortByKey': 'relevance'},
              'sort-citations': {'displayName': 'Citations', 'sortByKey': 'num_citations'},
              'sort-year': {'displayName': 'Year', 'sortByKey': 'year'},
            },
          }
        },
        methods: {
          searchQuery() {
            console.log("Query string: ", this.queryString);
            this.loadingState = true;
            searchPaperService.searchPaper(this.queryString, this.page, this.pageSize)
            .then(response => {
              console.log("RESPONSE: " + response.data);
              this.documents = response.data.response;
              this.totalPageResults = response.data.total_results;
              console.log(this.documents);
              this.loadingState = false;
            });
          },
        },
        created: function() {
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

.spinner {
  text-align: center;
  margin: auto;
}

[v-cloak] {
  display: none;
}
</style>
