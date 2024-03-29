<template>
    <v-container fluid class="document-result">
        <v-row no-gutters>
            <v-col cols="12" class="result-title">
                <nuxt-link :to="{ path: docUrl }">
                    <h4 class="font-weight-medium">{{ title }}</h4>
                </nuxt-link>
            </v-col>
            <v-col cols="6" class="result-type">
                {{ type }}
            </v-col>
        </v-row>

        <v-row no-gutters>
            <v-col class="result-info">
                <h6>{{ authors.join(', ') }} - {{ year }}</h6>
                <p v-if="abstract">{{ abstract.slice(0, 200) }}...</p>
            </v-col>
        </v-row>

        <v-row no-gutters>
            <v-col cols="4" class="citations">
                <nuxt-link :to="{ path: showCitingUrl }">
                    Cited by {{ nCitedBy }} ({{ nSelfCites }} self-citations)
                </nuxt-link>
            </v-col>
            <v-col cols="8" class="links">
                <a href="http://google.com">+Cite</a>
                <a v-if="docId" :href="pdfUrl" target="_blank">+View PDF</a>
                <a href="http://google.com">+Save</a>
                <a href="http://google.com">+Add to ExportCart</a>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: 'DocResultsItem',
    props: {
        docId: { type: String, default: '' },
        clusterId: { type: String, default: '' },
        title: { type: String, default: '' },
        type: { type: String, default: '' },
        authors: { type: Array, default: null },
        year: { type: String, default: '' },
        abstract: { type: String, default: '' },
        nCitedBy: { type: Number, default: 0 },
        nSelfCites: { type: Number, default: 0 }
    },
    computed: {
        docUrl() {
            if (this.docId) {
              return `/doc_view/pid/${this.docId}`;
            }

            return `/doc_view/cid/${this.clusterId}`;
        },

        pdfUrl() {
            return '/pdf/' + this.docId;
        },
        showCitingUrl() {
            return '/show_citing/' + this.clusterId;
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
