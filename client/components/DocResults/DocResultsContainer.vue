<template>
    <b-container class="document-results-container">
        <b-row class="document-results-header">
            <b-col sm="6">
                Results {{ (page - 1) * pageSize + 1 }} -
                {{
                    Math.min((page - 1) * pageSize + pageSize, totalPageResults)
                }}
                of {{ totalPageResults }}
            </b-col>
            <b-col sm="6">
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
                                >
                                    {{ item.displayName }}
                                </b-dropdown-item>
                            </li>
                        </ul>
                    </b-dropdown>
                </div>
            </b-col>
        </b-row>

        <doc-results-list :documents="documents" />
    </b-container>
</template>

<script>
import DocResultsList from './DocResultsList.vue';

export default {
    name: 'DocResultsContainer',
    components: {
        DocResultsList
    },
    props: {
        documents: { type: Array, default: null },
        totalPageResults: { type: Number, default: 0 },
        page: { type: Number, default: 0 },
        sortDropdown: { type: Object, default: null }
    },
    data() {
        return {
            pageSize: 10,
            sortByDisplay: 'Relevance'
        };
    },
    computed: {
        currentPageLocation() {
            return this.pageSize * (this.currentPage - 1) + 1;
        }
    },
    methods: {
        sortResults(event) {
            this.sortByDisplay = event.target.text;
            this.$emit('input', event.target.name);
        }
    }
};
</script>

<style scoped>
.document-results-container {
    background-color: lightgrey;
    margin-bottom: 2em;
    padding: 0.5em;
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
