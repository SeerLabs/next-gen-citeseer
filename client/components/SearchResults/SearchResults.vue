<template>
    <div v-cloak>
        <b-row>
            <b-col v-if="loadingState" md="8">
                <b-spinner class="spinner" label="Loading..." />
            </b-col>
            <b-col v-else id="search-results-list" md="8">
                <doc-results-container
                    v-model="sortBy"
                    :documents="documents"
                    :total-page-results="totalPageResults"
                    :page="page"
                    :sort-dropdown="sortDropdown"
                />
                <b-pagination
                    v-model="page"
                    :total-rows="totalPageResults"
                    :per-page="pageSize"
                    @input="searchQuery"
                />
            </b-col>
            <b-col id="search-results-cards" md="4">
                <search-results-filter />
                <search-results-external-links />
            </b-col>
        </b-row>
    </div>
</template>

<script>
import DocResultsContainer from '../DocResults/DocResultsContainer.vue';
import SearchResultsFilter from './SearchResultsFilter.vue';
import SearchResultsExternalLinks from './SearchResultsExternalLinks';
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
            sortDropdown: {
                'sort-relevance': {
                    displayName: 'Relevance',
                    sortByKey: 'relevance'
                },
                'sort-citations': {
                    displayName: 'Citations',
                    sortByKey: 'num_citations'
                },
                'sort-year': { displayName: 'Year', sortByKey: 'year' }
            },
            error: false
        };
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
                    console.log(error.message);
                    this.error = true;
                });
        }
    }
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
