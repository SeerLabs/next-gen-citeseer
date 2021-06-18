<template>
    <v-row id="doc-view-header">
        <v-col cols="9">
            <h2>{{ title }}</h2>
            <h5>{{ authors.join(', ') }}</h5>
            <h5>{{ venue }} - {{ year }}</h5>
            <br />

            <div
                id="abstract"
                :style="
                    showAbstract
                        ? { height: 'min-content' }
                        : { maxHeight: '150px' }
                "
            >
                <p>{{ abstract }}</p>
            </div>
            <v-btn @click="() => (showAbstract = !showAbstract)">
                {{ !showAbstract ? 'Show more' : 'Show less' }}
            </v-btn>
        </v-col>
        <v-col cols="3">
            <v-card id="document-options">
                <v-card-text>
                    <!-- PDF Button -->
                    <v-btn
                        id="pdf-btn"
                        squared
                        :href="getPDFUrl"
                        target="_blank"
                        class="mv-md-2"
                    >
                        View PDF
                    </v-btn>

                    <!-- Download Links Drop Down -->
                    <!--
                    <v-dropdown
                        id="download-links-dropdown"
                        text="Download Links"
                        variant="outline-secondary"
                        class="mv-md-4"
                        size="sm"
                    >
                        <v-dropdown-item>Link 1</v-dropdown-item>
                        <v-dropdown-item>Link 2</v-dropdown-item>
                        <v-dropdown-item>Link 3</v-dropdown-item>
                    </v-dropdown>
                    -->
                    <h6>Cite This</h6>
                    <h6>Save</h6>
                    <h6>Add to Collection</h6>
                    <h6>Add to MetaCart</h6>
                    <h6>Correct Errors</h6>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
export default {
    props: {
        docId: { type: String, default: '' },
        title: { type: String, default: '' },
        authors: { type: Array, default: null },
        venue: { type: String, default: '' },
        year: { type: String, default: '' },
        nCitation: { type: Number, default: 0 },
        abstract: { type: String, default: '' }
    },
    data() {
        return {
            showAbstract: false
        };
    },
    computed: {
        getPDFUrl() {
            return '/pdf/' + this.$route.params.id;
        }
    },
    methods: {
        toggleReadMore() {
            this.showAbstract = !this.showAbstract;
        }
    }
};
</script>

<style>
#doc-view-layout {
    background: rgb(255, 255, 255);
}

#doc-view-header {
    margin-bottom: 3em;
    background: #ffffff;
}

#abstract {
    overflow: hidden;
}

#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
}

.citation-card {
    margin-bottom: 1em;
}

#pdf-btn {
    background: rgb(235, 0, 0);
    color: white;
    margin-bottom: 1em;
    outline: transparent;
    border-color: transparent;
}
</style>
