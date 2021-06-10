<template>
    <div class="document-results-list">
        <ul>
            <li v-for="(item, index) in documents" :key="item.id">
                 <v-container fluid class="document-results-item">
                    <v-row no-gutters>
                        <v-col cols="11" class="result-title">
                            <nuxt-link :to="{ path: '/doc_view/pid/' + item.id }">
                                <h4 class="font-weight-medium">{{ item.title }}</h4>
                            </nuxt-link>
                        </v-col>
                        <v-col>
                        <button type="button" class="close" aria-label="Close" @click="$emit('remove-paper', index)">
                                <span aria-hidden="true">×</span>
                            </button>
                        </v-col>
                        <v-col cols="6" class="result-type">
                            {{ item.type }}
                        </v-col>
                    </v-row>

                    <v-row no-gutters>
                        <v-col class="result-info">
                            <h6>{{ item.authors.join(', ') }} - {{ item.year }}</h6>
                            <p v-if="item.abstract">{{ item.abstract.slice(0, 200) }}...</p>
                        </v-col>
                    </v-row>

                    <v-row no-gutters>
                        <v-col cols="4" class="citations">
                            Cited by {{ item.n_cited_by }} ({{ item.n_self_cites }} self-citations)
                        </v-col>
                        <v-col cols="8" class="links">
                            <a href="http://google.com">+Cite</a>
                            <a :href="'/pdf/' + item.id" target="_blank">+View PDF</a>
                            <a href="http://google.com">+Add to ExportCart</a>
                        </v-col>
                    </v-row>
                </v-container>
                
            </li>
        </ul>
    </div>
</template>

<script>

export default {
    name: 'DocResultsList',
    props: {
        documents: { type: Array, default: null }
    }
    // computed: {
    //     docUrl() {
    //         return `/doc_view/pid/${this.docId}`;
    //     },

    //     pdfUrl() {
    //         return '/pdf/' + this.docId;
    //     }
    // }
};
</script>

<style scoped>
.document-results-list {
    margin: 1.5em 0 1em 0;
    padding: 0;
}

.document-results-list ul {
    list-style: none;
    padding-left: 0;
}

.document-results-item {
    margin: 0.5em 0;
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