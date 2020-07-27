<template>
    <b-container fluid="sm" class="document-result">
        <b-row>
            <b-col class="result-title">
                <h5>
                    <nuxt-link :to="'/show_citing/' + cid">
                        {{ title }}
                    </nuxt-link>
                </h5>
            </b-col>
        </b-row>

        <b-row>
            <b-col class="result-info">
                <h6>
                    {{ authors || 'No authors available' }} -
                    {{ venue || 'No venue available' }} -
                    {{ year || 'No year available' }}
                </h6>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    name: 'CitationItem',
    props: {
        title: { type: String, default: '' },
        authors: { type: String, default: 'No authors available' },
        venue: { type: String, default: 'No venue available' },
        year: { type: Number, required: 0 },
        numCitations: { type: Number, default: 0 },
        cid: { type: Number, required: true }
    },
    data() {
        return {
            readMoreToggle: false,
            url: ''
        };
    },
    methods: {
        toggleReadMore() {
            this.readMoreFlag = true;
        }
    }
};
</script>

<style scoped>
.document-result {
    background-color: white;
    padding: 1rem;
    border-bottom: 1px solid gray;
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
