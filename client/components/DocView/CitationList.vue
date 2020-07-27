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

        <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            @input="getCitationEntities()"
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
            perPage: 5,
            currentPage: 1,
            citations: []
        };
    },
    computed: {
        rows() {
            return this.citations.length;
        }
    },
    mounted() {
        this.getCitationEntities();
    },
    methods: {
        getCitationEntities() {
            docViewService
                .getCitationsEntities(this.docId, this.currentPage)
                .then(response => (this.citations = response.data.citations))
                .catch(error => {
                    console.log(error);
                });
            console.log('Finished');
        }
    }
};
</script>
<style>
.hidden_header {
    display: none;
}
</style>
