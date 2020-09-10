<template>
    <v-container id="document-results-sorting" class="document-results-container">
        <v-row no-gutters class="document-results-header">
            <v-col sm="9">
                Results {{ (page - 1) * pageSize + 1 }} -
                {{
                Math.min((page - 1) * pageSize + pageSize, totalPageResults)
                }}
                of {{ totalPageResults }}
            </v-col>
            <v-col sm="3">
                <v-select
                    class="my-2 results-dropdown"
                    :items="sortDropdown"
                    :value="sortDropdown[0]"
                    label="Sort By"
                    outlined
                    dense
                    target="#document-results-sorting"
                />
            </v-col>
        </v-row>

        <doc-results-list :documents="documents" />
    </v-container>
</template>

<script>
import DocResultsList from './DocResultsList.vue';

export default {
    name: 'DocResultsContainer',
    components: {
        DocResultsList: DocResultsList
    },
    props: {
        documents: { type: Array, default: null },
        totalPageResults: { type: Number, default: 0 },
        page: { type: Number, default: 0 },
        sortDropdown: { type: Array, required: true }
    },
    data: function() {
        return {
            pageSize: 10,
            sortByDisplay: 'Relevance'
        };
    },
    computed: {
        currentPageLocation: function() {
            return this.pageSize * (this.currentPage - 1) + 1;
        }
    },
    methods: {
        sortResults: function(event) {
            this.sortByDisplay = event.target.text;
            this.$emit('input', event.target.name);
        }
    }
};
</script>

<style scoped>
.document-results-container {
    background-color: lightgrey;
    margin-bottom: 2em;
    padding: 0.5em;
}

.document-results-sorting {
    text-align: right;
}

.results-dropdown {
    cursor: pointer !important;
}
</style>
