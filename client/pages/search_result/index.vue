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
                <search-results-filter
                    class="mb-md-10"
                    :query-string="queryString"
                    @year-change="value => onYearFacetChange(value)"
                    @facet-change="({key, filters}) => onFacetChange(key, filters)"
                />
                <search-results-external-links />
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
            error: false,
            filters: {
                years: { start: 0, end: new Date().getFullYear() },
                authors: [],
                publishers: []
            },
            includePdfs: false
        };
    },
    computed: {
        totalNumRows() {
            return Math.ceil(this.totalPageResults / this.pageSize);
        }
    },
    watch: {
        '$route.query'() {
            this.queryString = this.$route.query.query;
            this.includePdfs = this.$route.query.pdf || true;
            this.searchQuery();
        }
    },
    created() {
        // make search query immediately when page is loaded
        this.queryString = this.$route.query.query;
        this.includePdfs = this.$route.query.pdf || true;
        this.searchQuery();
    },
    methods: {
        ...mapActions(['searchPaper']),
        searchQuery() {
            this.loadingState = true;
            // push params            
            const query = {
              queryString: this.queryString,
              page: this.page,
              pageSize: this.pageSize,
              yearStart: String(this.filters.years.start),
              yearEnd: String(this.filters.years.end),
              author: this.filters.authors,
              publisher: this.filters.publishers,
              includePdfs: this.includePdfs
            }

            this.searchPaper(query)
                .then(res => {
                    this.documents = res.response;
                    this.totalPageResults = Math.ceil(Math.min(res.total_results, 10000) / this.pageSize);
                    this.loadingState = false;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                });
        },

        onYearFacetChange(value) {
            this.filters.years.start = value[0];
            this.filters.years.end = value[1];

            this.searchQuery();
        },

        onFacetChange(key, filters) {
            this.filters[key] = filters;
            this.searchQuery();
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
