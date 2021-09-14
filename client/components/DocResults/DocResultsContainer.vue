<template>
    <v-container id="document-results-sorting" class="document-results-container">
        <v-row no-gutters class="document-results-header">
            <v-col sm="9">
                Results {{ (page - 1) * pageSize + 1 }} -
                {{
                Math.min((page - 1) * pageSize + pageSize, totalResults * pageSize)
                }}
                of {{ totalResults }}
            </v-col>
            <v-col sm="3">
                <v-select
                    v-model="sortBy"
                    class="my-2 results-dropdown"
                    :items="sortDropdown"
                    item-text="text"
                    item-value="sortByKey"
                    label="Sort By"
                    outlined
                    dense
                />
            </v-col>
        </v-row>
        <div v-if="loading" id="loading">
            <v-progress-linear rounded indeterminate color="teal" />
        </div>
        <doc-results-list v-else :documents="documents" />
    </v-container>
</template>

<script>
import DocResultsList from './DocResultsList.vue';

export default {
    name: 'DocResultsContainer',
    components: {
        DocResultsList
    },
    props: {
        documents: { type: Array, default: null },
        totalResults: { type: Number, default: 0 },
        page: { type: Number, default: 0 },
        sortDropdown: { type: Array, required: true },
        loading: {type: Boolean, default: false }
    },
    data() {
        return {
            pageSize: 10,
            sortBy: this.sortDropdown[0].sortByKey
        };
    },
    computed: {
        currentPageLocation() {
            return this.pageSize * (this.currentPage - 1) + 1;
        }
    },
    watch: {
        sortBy() {
            this.$emit('input', this.sortBy);
        }
    }
};
</script>

<style scoped>
.document-results-container {
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
