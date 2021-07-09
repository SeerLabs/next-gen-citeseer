<template>
    <div v-cloak>
        <v-row>
            <v-col v-if="loadingState" md="8">
                <v-progress-linear rounded indeterminate color="teal" />
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
                    :length="totalPageResults"
                    :total-visible="8"
                    @input="searchQuery"
                />
            </v-col>
            <v-col id="search-results-cards">
                <search-results-filter class="mb-md-10" />
                <search-results-external-links 
                    :query="queryString"
                />
            </v-col>
        </v-row>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import DocResultsContainer from '../../components/DocResults/DocResultsContainer';
import SearchResultsFilter from '../../components/SearchResults/SearchResultsFilter.vue';
import SearchResultsExternalLinks from '../../components/SearchResults/SearchResultsExternalLinks';


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
        ...mapActions(['searchPaper']),
        searchQuery() {
            this.loadingState = true;
            // push params
            this.searchPaper( {queryString: this.queryString, page: this.page, pageSize: this.pageSize} )
                .then(res => {
                    this.documents = res.response;
                    this.totalPageResults = Math.ceil(Math.min(res.total_results, 10000) / this.pageSize);
                    this.loadingState = false;
                })
                .catch(error => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                });
        }
    },
    layout: 'search'
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
