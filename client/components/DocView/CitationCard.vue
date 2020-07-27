<template>
    <b-card>
        <span v-if="true">
            <div class="citation-card-header">
                <div>
                    <h4>{{ title }}</h4>
                    <h6>{{ nCitations || 0 }} {{ title.toLowerCase() }}</h6>
                </div>
                <div class="document-results-sorting">
                    Sort by
                    <b-dropdown variant="primary" class="m-2 results-dropdown">
                        <template v-slot:button-content>
                            {{ sortByDisplay }}
                        </template>

                        <ul>
                            <li v-for="(item, key) in sortDropdown" :key="key">
                                <b-dropdown-item
                                    :name="key"
                                    @click="sortResults"
                                    >{{ item.displayName }}</b-dropdown-item
                                >
                            </li>
                        </ul>
                    </b-dropdown>
                </div>
            </div>
            <citation-list :doc-id="docId" :type="title" />
        </span>
        <b-card-text v-else class="my-5 text-center text-muted">
            <h3 class="md-3">No {{ title.toLowerCase() }} available</h3>
        </b-card-text>
    </b-card>
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
            sortDropdown: {},
            sortByKey: ''
        };
    },
    mounted() {
        switch (this.title) {
            case 'Citations':
                this.sortByDisplay = 'Relevance';
                this.sortDropdown = {
                    'sort-relevance': {
                        displayName: 'Relevance',
                        sortByKey: 'relevance'
                    },
                    'sort-Recency': {
                        displayName: 'Recency',
                        sortByKey: 'Recency'
                    }
                };
                this.sortByKey = 'relevance';
                break;
            case 'Similar Articles':
                this.sortByDisplay = 'Co-Citation';
                this.sortDropdown = {
                    'sort-co-citation': {
                        displayName: 'Co-Citation',
                        sortByKey: 'co-citation'
                    },
                    'sort-active-bibliography': {
                        displayName: 'Active Bibliography',
                        sortByKey: 'active-bibliography'
                    }
                };
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

.document-results-sorting {
    text-align: right;
}

.results-dropdown li {
    list-style: none;
}

.results-dropdown ul {
    padding: 0;
}
</style>
