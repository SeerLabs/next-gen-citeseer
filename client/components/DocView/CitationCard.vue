<template>
    <v-card class="mb-10">
        <span v-if="true">
            <div class="citation-card-header">
                <div>
                    <v-card-title>{{ title }}</v-card-title>
                    <v-card-subtitle>
                        {{ nCitations || 0 }} {{ title.toLowerCase() }}
                    </v-card-subtitle>
                </div>
                <div class="citation-sorting-container">
                    <v-select
                        dense
                        class="m-2 citation-sorting"
                        :value="sortDropdown[0]"
                        :items="sortDropdown"
                        label="Sort By"
                        outlined
                    />
                </div>
            </div>
            <v-card-text>
                <citation-list :doc-id="docId" :type="title" />
            </v-card-text>
        </span>
        <v-card-text v-else class="text-center text-muted blue-grey lighten-4">
            <h3 class="pa-10">No {{ title.toLowerCase() }} available</h3>
        </v-card-text>
    </v-card>
</template>

<script>
import CitationList from './CitationList.vue';
export default {
    name: 'CitationCard',
    components: {
        CitationList
    },
    props: {
        docId: { type: String, default: '' },
        title: { type: String, default: '' },
        nCitations: { type: Number, default: 0 }
    },
    data() {
        return {
            sortByDisplay: '',
            sortDropdown: [],
            sortByKey: ''
        };
    },
    mounted() {
        switch (this.title) {
            case 'Citations':
                this.sortByDisplay = 'Relevance';
                this.sortDropdown = [
                    {
                        text: 'Relevance',
                        sortByKey: 'relevance'
                    },
                    {
                        text: 'Recency',
                        sortByKey: 'Recency'
                    }
                ];
                this.sortByKey = 'relevance';
                break;
            case 'Similar Articles':
                this.sortByDisplay = 'Co-Citation';
                this.sortDropdown = [
                    {
                        text: 'Co-Citation',
                        sortByKey: 'co-citation'
                    },
                    {
                        text: 'Active Bibliography',
                        sortByKey: 'active-bibliography'
                    }
                ];
                this.sortByKey = 'co-citation';
                break;
        }
    },
    methods: {
        sortResults(event) {
            const dropdownItem = event.target.name;
            this.sortByDisplay = event.target.text;
            this.sortByKey = this.sortDropdown[dropdownItem].sortByKey;
        }
    }
};
</script>

<style scoped>
.citation-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
}

div.citation-sorting-container {
    padding: 16px;
}

.citation-sorting {
    width: 150px;
    text-align: right;
}

.results-dropdown li {
    list-style: none;
}

.results-dropdown ul {
    padding: 0;
}
</style>
