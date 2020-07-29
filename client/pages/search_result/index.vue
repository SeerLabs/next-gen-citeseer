<template>
    <div v-cloak>
        <v-row>
            <v-col v-if="loadingState" md="8">
                <b-spinner class="spinner" label="Loading..." />
            </v-col>
            <v-col v-else id="search-results-list" md="8">
                <doc-results-container
                    v-model="sortBy"
                    :documents="documents"
                    :total-page-results="totalPageResults"
                    :page="page"
                    :sort-dropdown="sortDropdown"
                />
                <v-pagination
                    v-model="page"
                    :length="totalNumRows"
                    :total-visible="8"
                    @input="searchQuery"
                />
            </v-col>
            <v-col id="search-results-cards" md="4">
                <search-results-filter />
                <search-results-external-links />
            </v-col>
        </v-row>
    </div>
</template>

<script>
import DocResultsContainer from '../../components/DocResults/DocResultsContainer';
import SearchResultsFilter from '../../components/SearchResults/SearchResultsFilter.vue';
import SearchResultsExternalLinks from '../../components/SearchResults/SearchResultsExternalLinks';
import searchPaperService from '~/api/SearchPaperService';

export default {
    name: 'SearchResults',
    components: {
        DocResultsContainer,
        SearchResultsFilter,
        SearchResultsExternalLinks
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
            sortDropdown: [
                {
                    text: 'Relevance',
                    callback: () => (this.sortBy = 'relevance')
                },
                {
                    text: 'Citations',
                    callback: () => (this.sortBy = 'num_citations')
                },
                { text: 'Year', callback: () => (this.sortBy = 'year') }
            ],
            error: false
        };
    },
    computed: {
        totalNumRows() {
            return this.totalPageResults / this.pageSize;
        }
    },
    watch: {
        '$route.query.query'() {
            this.queryString = this.$route.query.query;
            this.searchQuery();
        }
    },
    created() {
        // make search query immediately when page is loaded
        this.queryString = this.$route.query.query;
        this.searchQuery();
    },
    methods: {
        searchQuery() {
            this.loadingState = true;
            // push params
            searchPaperService
                .searchPaper(this.queryString, this.page, this.pageSize)
                .then(response => {
                    this.documents = response.data.response;
                    this.totalPageResults = response.data.total_results;
                    this.loadingState = false;
                })
                .catch(error => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                });
        }
    },
    layout: 'layout_search'
};
</script>

<style>
.search-result {
    margin-bottom: 0.5em;
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
