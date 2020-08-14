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
                    <template v-slot:prepend>{{ yearRange[0] }}</template>
                    <template v-slot:append>{{ yearRange[1] }}</template>
                </v-range-slider>
            </div>

            <v-menu
                v-for="facet in facets"
                :key="facet.key"
                v-model="facet.menu"
                :close-on-content-click="false"
                bottom
                offset-y
                transition="scale-transition"
            >
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        color="indigo"
                        dark
                        v-bind="attrs"
                        class="facet-menu"
                        v-on="on"
                        >{{ facet.key.toUpperCase() }}</v-btn
                    >
                </template>
                <v-card>
                    <v-list>
                        <v-list-item
                            v-for="item in facet.items"
                            :key="item.key"
                        >
                            <v-list-item-action>
                                <v-checkbox
                                    :id="item.key"
                                    v-model="facet.filter"
                                    type="checkbox"
                                    :value="item.key"
                                    :label="`${item.key} (${item.doc_count})`"
                                    class="facet-checkbox"
                                    @change="
                                        $emit('facet-change', {
                                            key: facet.key,
                                            filter: facet.filter
                                        })
                                    "
                                />
                            </v-list-item-action>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-menu>
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

            facets: []
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
                    response.data.aggs.forEach(agg => {
                        this.facets = [
                            ...this.facets,
                            {
                                ...agg,
                                filter: [],
                                menu: false
                            }
                        ];
                    });

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
.facet-menu {
    margin-top: 1rem;
    width: 7vw;
}
</style>

<style>
.facet-checkbox .v-label {
    margin-bottom: 0 !important;
    margin-left: 0.5rem;
}
</style>
