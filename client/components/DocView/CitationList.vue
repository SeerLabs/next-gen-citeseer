<template>
    <div class="overflow-auto">
        <citation-item
            v-for="(citation, index) in citations"
            id="citation-list"
            :key="index"
            :title="citation.title"
            :year="citation.year"
            :authors="citation.authors"
            :venue="citation.venue"
            :cid="citation.cluster"
        />

        <p class="mt-3">Current Page: {{ currentPage }}</p>

        <v-pagination
            v-model="currentPage"
            :total-visible="6"
            :length="totalNumRows"
            @input="getCitationEntities"
        />
    </div>
</template>

<script>
import CitationItem from './CitationItem';
import docViewService from '~/api/DocViewService';

export default {
    name: 'CitationList',
    components: {
        CitationItem
    },
    props: {
        docId: { type: String, default: '' },
        doi: { type: String, default: '' },
        type: { type: String, default: '' }
    },
    data() {
        return {
            perPage: 10,
            currentPage: 1,
            citations: [],
            nCitations: 0
        };
    },
    computed: {
        totalNumRows() {
            return this.nCitations / this.perPage;
        }
    },
    created() {
        this.getCitationEntities();
    },
    methods: {
        getCitationEntities() {
            docViewService
                .getCitationsEntities(
                    this.docId,
                    this.currentPage,
                    this.perPage
                )
                .then(response => {
                    this.citations = response.data.citations;
                    this.nCitations = response.data.total_results;
                })
                .catch(error => {
                    // eslint-disable-next-line
                    console.log(error);
                });
        }
    }
};
</script>
<style>
.hidden_header {
    display: none;
}
</style>
