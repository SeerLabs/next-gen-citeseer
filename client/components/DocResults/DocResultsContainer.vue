<template>
    <v-container id="document-results-sorting" class="document-results-container pa-0">
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
        loading: {type: Boolean, default: false }
    },
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
