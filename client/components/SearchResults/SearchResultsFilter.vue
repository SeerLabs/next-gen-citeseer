<template>
    <v-card id="search-results-filter" outlined>
        <v-toolbar flat dense color="primary"><h5 class="white--text ma-0">Filter results</h5></v-toolbar>
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
                    thumb-color="#a9a9a9"
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
                    >{{facet.key.toUpperCase()}}</v-btn>
                </template>
                <v-card>
                    <v-card-title>{{ facet.key.charAt(0).toUpperCase() + facet.key.slice(1) }}</v-card-title>
                    <v-list>
                        <v-list-item>
                          <v-text-field
                            v-model="facet.searchQuery"
                            :label="`Search ${facet.key}`"
                            outlined
                            dense
                            @keydown.enter="searchFilter(facet)"
                          />
                        </v-list-item>
                        <v-list-item v-for="item in facet.items" :key="item.key">
                            <v-list-item-action>
                                <v-checkbox
                                    :id="item.key"
                                    v-model="facet.filter"
                                    type="checkbox"
                                    :value="item.key"
                                    :label="`${item.key} ${item.doc_count ? '(' + item.doc_count + ')' : ''}`"
                                    class="facet-checkbox"
                                    @change="$emit('facet-change', {key: facet.key, filters: facet.filter})"
                                >
                                    <v-icon 
                                      v-if="!item.doc_count"
                                      slot="append"
                                      @click="removeItem(facet, item)"
                                    >
                                      cancel
                                    </v-icon>
                                </v-checkbox>
                            </v-list-item-action>
                        </v-list-item>
                    </v-list>
                </v-card>
            </v-menu>
        </v-card-text>
    </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'SearchResultsFilter',
    props: {
        queryString: { type: String, default: '' }
    },
    data() {
        const yearMin = 1931;
        const yearMax = new Date().getFullYear();

        return {
            loadingState: false,

            yearMin,
            yearMax,
            yearRange: [yearMin, yearMax],

            facets: [],
        };
    },
    watch: {
        queryString() {
            this.populateFacets();
        }
    },
    mounted() {
        // make search query immediately when page is loaded
        this.populateFacets();
    },
    methods: {
        ...mapActions(['getAggregations']),
        populateFacets() {
            this.loadingState = true;

            this.getAggregations({queryString: this.queryString})
                .then((response) => {
                    const aggregations = response.aggregations.agg

                    if ('authors_fullname_terms' in aggregations) {
                      this.facets = [
                     
                        {
                          key: 'authors',
                          items: aggregations.authors_fullname_terms,
                          filter: [],
                          searchQuery: "",
                          menu: false
                        }
                      ]
                    }

                    this.loadingState = false;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                });
        },

        searchFilter(facet) {

          const searchQuery = facet.searchQuery;

          if (facet.items.filter(item => item.key === searchQuery).length === 0) {
            facet.items.push({key: searchQuery});
          }
          facet.filter.push(searchQuery);

          this.$emit('facet-change', {key: facet.key, filters: facet.filter})
          facet.searchQuery = "";
        },

        removeItem(facet, item) {
          facet.items = facet.items.filter(i => i.key !== item.key);
          facet.filter = facet.filter.filter(i => i !== item.key);
          this.$emit('facet-change', {key: facet.key, filters: facet.filter});
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
