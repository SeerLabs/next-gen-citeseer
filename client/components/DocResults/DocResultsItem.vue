<template>
    <b-container fluid="sm" class="document-result">
        <b-row>
            <b-col cols="12" class="result-title">
                <nuxt-link :to="{ path: `/doc_view/${docId}` }">
                    <h4>{{ title }}</h4>
                </nuxt-link>
            </b-col>
            <b-col cols="6" class="result-type">
                {{ type }}
            </b-col>
        </b-row>

        <b-row>
            <b-col class="result-info">
                <h6>{{ authors.join(', ') }} - {{ year }}</h6>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="result-content">
                <p>{{ abstract.slice(0, 200) }}...</p>
            </b-col>
        </b-row>

        <b-row>
            <b-col cols="3" class="citations">
                Cited by {{ numCitations }}
            </b-col>
            <b-col cols="9" class="links">
                <a href="http://google.com">+Cite</a>
                <a href="http://google.com">+View PDF</a>
                <a href="http://google.com">+Save</a>
                <a href="http://google.com">+Add to ExportCart</a>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'DocResultsItem',
    props: {
        docId: { type: String, default: '' },
        title: { type: String, default: '' },
        type: { type: String, default: '' },
        authors: { type: Array, default: null },
        year: { type: String, default: '' },
        abstract: { type: String, default: '' },
        numCitations: { type: Number, default: 0 }
    },
    computed: {
        docUrl() {
            return `/doc_view/${this.doc_id}`;
        }
    }
};
</script>

<style scoped>
.document-result {
    background-color: white;
    padding: 1rem;
}

.result-type {
    text-align: right;
    font-weight: 600;
}

.result-info {
    margin-bottom: 0.5em;
}

.result-content {
    margin-bottom: 0.3em;
}

.links {
    text-align: right;
}

.links a {
    margin-left: 1em;
}
</style>
