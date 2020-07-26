<template>
    <b-container fluid="sm" class="document-result">
        <b-row>
            <b-col cols="12" class="result-title">
                <nuxt-link :to="{ path: `/doc_view/${doc_id}` }">
                    <h4>{{ title }}</h4>
                </nuxt-link>
            </b-col>
            <b-col cols="6" class="result-type">{{ type }}</b-col>
        </b-row>

        <b-row>
            <b-col class="result-info">
                <h6>{{ authors.join(', ') }} - {{ year.toString() }}</h6>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="result-content">
                <p>{{ abstract.slice(0, 200) }}...</p>
            </b-col>
        </b-row>

        <b-row>
            <b-col cols="3" class="citations">Cited by {{ numCitations }}</b-col>
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
    name: 'DocumentResultsItem',
    props: {
        doc_id: String,
        title: String,
        type: String,
        authors: Array,
        year: String,
        abstract: String,
        numCitations: Number
    },
    computed: {
        docUrl: function () {
            return `/doc_view/${this.doc_id}`;
        }
    },
    created() {
        if (!this.$props.title) {
            this.$props.title = 'Title Not Indexed';
        }
        if (this.$props.authors.length == 0) {
            this.$props.authors = ['Authors Not Indexed'];
        }
        if (!this.$props.year || this.$props.year == 0) {
            this.$props.year = 'Year Not Indexed';
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
