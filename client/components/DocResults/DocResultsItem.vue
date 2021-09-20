<template>
    <v-container fluid class="document-result">
        <v-row no-gutters>
            <v-col cols="12" class="result-title">
                <nuxt-link :to="{ path: docUrl }">
                    <h5 class="text--primary">{{ title }}</h5>
                </nuxt-link>
            </v-col>
            <v-col cols="6" class="result-type">
                {{ type }}
            </v-col>
        </v-row>

        <v-row no-gutters>
            <v-col class="result-info">
                <p class="font-italic">{{ authors.join(', ') }} &bull; {{ year }}</p>
                <p v-if="abstract">{{ abstract.slice(0, 200) }}...</p>
            </v-col>
        </v-row>

        <v-row no-gutters justify="space-between">
            <v-col cols="6">
                <nuxt-link :to="{ path: showCitingUrl }" class="citation">
                    Cited by <span class="accent--text">{{ nCitedBy }} Documents</span> &bull; {{ nSelfCites }} self-citations
                </nuxt-link>
            </v-col>

            <v-col cols="6" class="links" align="end">

                <!-- TODO: Move the dialog to single component -->
                <v-dialog
                    max-width="40%"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <button class="ml-4" v-bind=attrs v-on=on>
                            <v-icon dense>format_quote</v-icon>Cite
                        </button>
                    </template>
                    <v-card class="pa-5">
                        <v-card-title>
                            Cite This Paper
                        </v-card-title>
                        <v-card-text>
                            <v-container>
                                <v-row>
                                    <textarea 
                                    id="bibtex"
                                    :value="bibtex"
                                    ></textarea>
                                </v-row>
                            </v-container>
                        </v-card-text>
                  
                        <v-card-actions>
                            <v-btn
                                color="primary"
                                @click="copyBibtex"
                            >
                                <v-icon left>content_copy</v-icon>
                                {{ copied ? 'Copied!' : 'Copy' }}
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-dialog>

                <nuxt-link :to=pdfUrl target="_blank">
                    <button class="ml-4">
                        <v-icon dense>description</v-icon>View PDF
                    </button>
                </nuxt-link>
          
                <add-to-collection-dialog
                    :doc-id="docId"
                    :collection-names="collectionNames"
                    :button-type="'searchItem'"
                />

                <button class="ml-4"><v-icon dense>shopping_cart</v-icon>Add to Cart</button>
            </v-col>

        </v-row>
    </v-container>
</template>

<script>

import AddToCollectionDialog from '~/components/MyCiteSeer/AddToCollectionDialog.vue'
export default {
    name: 'DocResultsItem',
    components: {
        AddToCollectionDialog
    },
     props: {
        docId: { type: String, default: '' },
        clusterId: { type: String, default: '' },
        title: { type: String, default: '' },
        type: { type: String, default: '' },
        authors: { type: Array, default: null },
        year: { type: String, default: '' },
        abstract: { type: String, default: '' },
        nCitedBy: { type: Number, default: 0 },
        nSelfCites: { type: Number, default: 0 },
        collectionNames: {type: Array, default: null}
    },
    data() {
        return {
            // Register if a bibtex is copied
            copied: false,
        }  
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
        },
        // TODO: Add in other fields required for a full bibtex
        bibtex() {
            return `@article{Citekey,` + 
            `\n\ttitle={${this.title}},` +
            `\n\tauthor={${this.authors.join(' and ')}},` +
            `\n\tyear={${this.year}}` +
            `\n\tjournal={}` +
            '\n}'
                    
        }
    },
    methods: {
        // Copy the generated Bibtex by clicking the copy button
        copyBibtex() {
            const textarea = document.getElementById("bibtex");
            textarea.select();
            document.execCommand("copy");
            this.copied = true;
        },
    }
};
</script>

<style scoped>
.document-result {
    background-color: white;
    padding: 1rem;
    border: 2px solid #eaeaea;
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

.links button {
    color: var(--v-secondary-darken5);
    font-weight: bold;
}

.links i {
    padding-right: 4px;
    vertical-align: middle;
}

.citation {
    color: var(--v-secondary-darken5);
    font-weight: bold;
}

#bibtex {
    width: 100%;
    min-height: 8rem;
    padding: 5px;

    background-color: #ededed;
    font-family: monospace;
    white-space: pre;
}
</style>
