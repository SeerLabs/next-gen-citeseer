<template>
    <v-card class="mb-10">
        <span v-if="true">
            <div class="citation-card-header">
                <div>
                    <v-card-title>{{ title }}</v-card-title>
                    <v-card-subtitle>
                        {{ nCitations || 0 }} {{ title.toLowerCase() }}
                    </v-card-subtitle>
                </div>
                <div class="citation-sorting-container">
                    <v-select
                        v-model="sortSelected"
                        dense
                        class="m-2 citation-sorting"
                        :items="sortDropdown"
                        label="Sort By"
                        outlined
                        @change="getCitations"
                    />
                </div>
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
import CitationList from './CitationList.vue';
import docViewService from '~/api/DocViewService';
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
            case 'Similar Articles':
                this.sortSelected = 'Co-Citation';
                this.sortDropdown = [
                    'Co-Citation',
                    'Active Bibliography',
                    'TF-IDF'
                ];
                this.getCitations();
                break;
        }
    },
    methods: {
        getCitations() {
            switch (this.title) {
                case 'Citations':
                    this.loading = true;
                    docViewService
                        .getCitationsEntities(
                            this.docId,
                            this.currentPage,
                            this.perPage
                        )
                        .then(response => {
                            this.citations = response.data.citations;
                            this.nCitations = response.data.total_results;
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
                    
                    docViewService
                        .getSimilarPaper(
                            queryId,
                            this.sortSelected
                        )
                        .then(response => {
                            this.citations = response.data.similar_papers;
                            this.nCitations = response.data.total_results;
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
.citation-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}

div.citation-sorting-container {
    padding: 16px;
}

.citation-sorting {
    width: 150px;
    text-align: right;
}

.results-dropdown li {
    list-style: none;
}

.results-dropdown ul {
    padding: 0;
}
</style>
