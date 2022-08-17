<template>
    <v-card class="mb-10" flat outlined rounded=0>
        <span v-if="true">
            <v-toolbar flat dense color="primary"><h5 class="white--text ma-0">{{ title }}</h5></v-toolbar>
                <div id="subtitle-container">
                    <v-container>
                        <v-row>
                            <v-col cols=10>
                                <v-card-subtitle>
                                    {{ nCitations || 0 }} {{ title.toLowerCase() }}
                                </v-card-subtitle>
                            </v-col>
                            <v-col>
                                <v-select
                                    v-model="sortSelected"
                                    dense
                                    class="m-2 citation-sorting"
                                    :items="sortDropdown"
                                    label="Sort By"
                                    outlined
                                    @change="getCitations"
                                />
                            </v-col>
                        </v-row>
                    </v-container>
                </div>
            <v-card-text>
                <div v-if="loading" id="loading">
                    <v-progress-linear rounded indeterminate color="teal" />
                </div>
                <div v-else>
                    <citation-list
                        :doc-id="docId"
                        :title="title"
                        :citations="citations"
                        :n-citations="nCitations"
                        :loading="loading"
                    />
                    <v-pagination
                        v-model="currentPage"
                        :total-visible="6"
                        :length="totalNumRows"
                        @input="getCitations"
                    />
                    <p class="mt-3">Current Page: {{ currentPage }}</p>
                </div>
            </v-card-text>
        </span>
        <v-card-text v-else class="text-center text-muted blue-grey lighten-4">
            <h3 class="pa-10">No {{ title.toLowerCase() }} available</h3>
        </v-card-text>
    </v-card>
</template>

<script>
import { mapActions } from 'vuex';
import CitationList from './CitationList.vue';

export default {
    name: 'CitationCard',
    components: {
        CitationList
    },
    props: {
        docId: { type: String, default: '' },
        cid: { type: String, default: ''},
        title: { type: String, default: '' }
    },
    data() {
        return {
            sortByDisplay: '',
            sortDropdown: [],
            sortSelected: '',
            citations: [],
            nCitations: 0,
            perPage: 10,
            currentPage: 1,
            loading: false
        };
    },
    computed: {
        totalNumRows() {
            return Math.floor(this.nCitations / this.perPage);
        }
    },
    created() {
        switch (this.title) {
            case 'Citations':
                this.sortSelected = 'Relevance';
                this.sortDropdown = [
                    'Relevance',
                    'Recency'
                ];

                this.getCitations();
                break;
            // case 'Similar Articles':
                // this.sortSelected = 'Co-Citation';
                // this.sortDropdown = [
                    // 'Co-Citation',
                    // 'Active Bibliography',
                    // 'TF-IDF'
                // ];
                // this.getCitations();
                // break;
        }
    },
    methods: {
        ...mapActions(['getCitationsEntities', 'getSimilarPaper']),

        getCitations() {
            switch (this.title) {
                case 'Citations':
                    this.loading = true;
                    this.getCitationsEntities({
                            id: this.docId,
                            page: this.currentPage,
                            pageSize: this.perPage
                        })
                        .then(response => {
                            this.citations = response.citations;
                            this.nCitations = response.total_results;
                            this.loading = false;
                        })
                        .catch(error => {
                            this.loading = false;
                            // eslint-disable-next-line
                            console.log(error);
                        });
                    break;
                case 'Similar Articles': {
                    this.loading = true;
                    let queryId = this.cid;
                    if (this.sortSelected === 'TF-IDF'){
                        queryId = this.docId;
                    }
                    this.getSimilarPaper({
                        id: queryId,
                        algo: this.sortSelected
                    })
                        .then(response => {
                            this.citations = response.similar_papers;
                            this.nCitations = response.total_results;
                            this.loading = false;
                        })
                        .catch(error => {
                            this.loading = false;
                            // eslint-disable-next-line
                            console.log(error);
                        });
                    break;
                }
            }
        }
    }
};
</script>

<style scoped>

#subtitle-container {
    border-bottom: 1px solid var(--v-secondary-lighten5);
}

.results-dropdown li {
    list-style: none;
}

.results-dropdown ul {
    padding: 0;
}
</style>
