<template>
    <b-row id="doc-view-header">
        <b-col cols="9">
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

            <b-button @click="() => (showAbstract = !showAbstract)">
                {{ !showAbstract ? 'Show more' : 'Show less' }}
            </b-button>
        </b-col>
        <b-col cols="3">
            <b-card id="document-options">
                <b-card-text>
                    <!-- PDF Button -->
                    <b-button
                        id="pdf-btn"
                        squared
                        :to="getPDFUrl"
                        target="_blank"
                        class="mb-md-2"
                    >
                        View PDF
                    </b-button>

                    <!-- Download Links Drop Down -->
                    <b-dropdown
                        id="download-links-dropdown"
                        text="Download Links"
                        variant="outline-secondary"
                        class="mb-md-4"
                        size="sm"
                    >
                        <b-dropdown-item>Link 1</b-dropdown-item>
                        <b-dropdown-item>Link 2</b-dropdown-item>
                        <b-dropdown-item>Link 3</b-dropdown-item>
                    </b-dropdown>
                    <h6>Cite This</h6>
                    <h6>Save</h6>
                    <h6>Add to Collection</h6>
                    <h6>Add to MetaCart</h6>
                    <h6>Correct Errors</h6>
                </b-card-text>
            </b-card>
        </b-col>
    </b-row>
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
    margin-top: 3em;
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
    outline: transparent;
    border-color: transparent;
}
</style>
