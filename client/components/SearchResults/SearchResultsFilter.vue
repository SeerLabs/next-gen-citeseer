<template>
    <v-card id="search-results-filter">
        <v-card-title>Filter results</v-card-title>
        <v-card-text>
            <div class="d-flex justify-space-between">
                <h6>Year</h6>
            </div>
            <div>
                <v-range-slider
                    v-model="yearRange"
                    :max="yearMax"
                    :min="yearMin"
                    hide-details
                    class="align-center"
                    @change="$emit('year-change', yearRange)"
                >
                    <template v-slot:prepend>
                        {{ yearRange[0] }}
                    </template>
                    <template v-slot:append>
                        {{ yearRange[1] }}
                    </template>
                </v-range-slider>
            </div>
            <div>
                <h6>Authors</h6>
                <div v-for="author in authors" :key="author.key">
                    <input
                        :id="author.key"
                        v-model="authorFilter"
                        type="checkbox"
                        :value="author.key"
                        @change="$emit('author-change', authorFilter)"
                    />
                    <label :for="author.key">
                        {{ author.key }} ({{ author.doc_count }})
                    </label>
                </div>
            </div>
        </v-card-text>
    </v-card>
</template>

<script>
import searchPaperService from '~/api/SearchPaperService';

export default {
    name: 'SearchResultsFilter',
    props: {
        queryString: { type: String, default: '' }
    },
    data() {
        const yearMin = 0;
        const yearMax = new Date().getFullYear();

        return {
            loadingState: false,

            yearMin,
            yearMax,
            yearRange: [yearMin, yearMax],

            authors: [],
            authorFilter: []
        };
    },
    watch: {
        queryString() {
            this.getAggregations();
        }
    },
    created() {
        // make search query immediately when page is loaded
        this.getAggregations();
    },
    methods: {
        getAggregations() {
            this.loadingState = true;

            searchPaperService
                .getAggregations(this.queryString)
                .then(response => {
                    this.authors = response.data.authors;
                    this.loadingState = false;
                })
                .catch(error => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                });
        }
    }
};
</script>

<style scoped>
#search-results-filter {
    margin-bottom: 20px !important;
}

#year-filter-value {
    text-align: right;
}
</style>
