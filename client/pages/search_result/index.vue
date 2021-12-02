<template>
    <div v-cloak id="search-results-container">
        <v-container>
             <v-row align="center" class="px-2 mb-5">
                    <v-col md="6">
                        <p class="mb-0 font-weight-bold secondary--text">Results {{ (page-1) * pageSize + 1 }} - 
                        {{
                            Math.min((page - 1) * pageSize + pageSize, totalResults * pageSize)
                        }}
                        out of {{ totalResults }}
                        </p>
                    </v-col>
                    <v-col md="2">
                        <v-select
                            :items="sortDropdown"
                            label="Sort By"
                            outlined
                            dense
                            hide-details
                            @input="searchQuery"
                        />
                    </v-col>
                </v-row>
        <v-row>
            <v-col v-if="loadingState" md="8">
                <v-progress-linear rounded indeterminate/>
            </v-col>
            <v-col v-else md="8">
                <doc-results-container
                    v-model="sortBy"
                    :documents="documents"
                    :total-results="totalResults"
                    :page="page"

                />
                <v-pagination
                    v-model="page"
                    :length="totalPages"
                    :total-visible="8"
                    @input="searchQuery"
                />
            </v-col>
            <v-col id="search-results-cards" md="4">
                <search-results-filter
                    class="mb-md-10"
                    :query-string="queryString"
                    @year-change="value => onYearFacetChange(value)"
                    @facet-change="({key, filters}) => onFacetChange(key, filters)"
                />
                <search-results-external-links :query="queryString"/>
            </v-col>
        </v-row>
        </v-container>
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
            totalResults: 0,
            // Number of results displayed on one page
            pageSize: 10,
            // Current page number
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
                { 
                    text: 'Year', 
                    callback: () => (this.sortBy = 'year') 
                }
            ],
            error: false,
            filters: {
                years: { start: 1913, end: new Date().getFullYear() },
                authors: [],
                publishers: []
            },
            includePdfs: false
        };
    },
    computed: {
        totalPages() {
            return Math.ceil(this.totalResults / this.pageSize);
        },
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
              sortBy: this.sortBy,
              yearStart: String(this.filters.years.start),
              yearEnd: String(this.filters.years.end),
              author: this.filters.authors,
              publisher: this.filters.publishers,
              includePdfs: this.includePdfs
            }

            this.searchPaper(query)
                .then(res => {
                    this.documents = res.response;
                    this.totalResults = Math.ceil(Math.min(res.total_results, 10000));
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

<style scoped>

#search-results-container {
    background-color: #F7F7F7;
    padding: 2rem 8rem;
    border-top: 2px solid #e0e0e0;
}

.spinner {
    text-align: center;
    margin: auto;
}

[v-cloak] {
    display: none;
}
</style>
