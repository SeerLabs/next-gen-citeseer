<template>
    <div class="document-result">
        <v-row no-gutters>
            <v-col class="result-title">
                <h5>
                    <nuxt-link v-if="inCollection && cid" :to="'/doc_view/cid/' + cid">
                        {{ title }}
                    </nuxt-link>
                    <nuxt-link v-else-if="cid" :to="'/show_citing/' + cid">
                        {{ title }}
                    </nuxt-link>
                    <span v-else>
                        {{ title || 'No title available' }}
                    </span>
                </h5>
            </v-col>
        </v-row>

        <v-row no-gutters>
            <v-col class="result-info">
                <h6>
                    {{ authors.join(", ") || 'No authors available' }} -
                    {{ venue || 'No venue available' }} -
                    {{ year || 'No year available' }}
                </h6>
            </v-col>
        </v-row>
    </div>
</template>

<script>
export default {
    name: 'CitationItem',
    props: {
        title: { type: String, default: '' },
        authors: { type: Array[String], default: 'No authors available' },
        venue: { type: String, default: 'No venue available' },
        year: { type: String, default: '0' },
        numCitations: { type: Number, default: 0 },
        cid: { type: String, required: true },
        inCollection: { type: Boolean, required: true }
    },
    data: function() {
        return {
            readMoreToggle: false,
            url: ''
        };
    },
    methods: {
        toggleReadMore: function() {
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
