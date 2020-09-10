<template>
    <div class="overflow-auto">
        <div v-if="loading" id="loading">
            <v-progress-linear rounded indeterminate color="teal" />
        </div>
        <div v-else>
            <citation-item
                v-for="(citation, index) in citations"
                id="citation-list"
                :key="index"
                :title="citation.title"
                :year="citation.year"
                :authors="citation.authors"
                :venue="citation.venue"
                :cid="citation.cluster"
                :in-collection="citation.in_collection"
            />

            

            <!-- <v-pagination
                v-model="currentPage"
                :total-visible="6"
                :length="totalNumRows"
                @input="getCitationEntities"
            /> -->
        </div>
    </div>
</template>

<script>
import CitationItem from './CitationItem';
// import docViewService from '~/api/DocViewService';

export default {
    name: 'CitationList',
    components: {
        CitationItem: CitationItem
    },
    props: {
        docId: { type: String, default: '' },
        cid: { type: String, default: null },
        doi: { type: String, default: '' },
        title: { type: String, default: '' },
        citations: {type:Array, default: null},
        nCitations: { type: Number, default: 0}
    },
    data: function() {
        return {
            // perPage: 10,
            // currentPage: 1,
            // citations: [],
            // nCitations: 0,
            loading: false
        };
    },
    computed: {
        // totalNumRows: function() {
        //     return this.nCitations / this.perPage;
        // }
    },
    created: function() {
        // switch (this.title){
        //     case 'Citations':
        //         this.getCitationEntities();
        //         break;
        //     case 'Similar Articles':
        //         this.getSimilarPapers('tf-idf');
        //         break;
        // }
    },
    methods: {
        // getCitationEntities: function() {
        //     this.loading = true;
        //     docViewService
        //         .getCitationsEntities(
        //             this.docId,
        //             this.currentPage,
        //             this.perPage
        //         )
        //         .then(response => {
        //             this.citations = response.data.citations;
        //             this.nCitations = response.data.total_results;
        //             this.loading = false;
        //         })
        //         .catch(error => {
        //             this.loading = false;

        //             // eslint-disable-next-line
        //             console.log(error);
        //         });
        // },
        // getSimilarPapers: function(algo) {
        //     this.loading = true;
        //     let id = '';
        //     if (algo === 'tf-idf'){
        //         id = this.docId;
        //     }
        //     else{
        //         id = this.cid;
        //     }
        //     docViewService
        //         .getSimilarPaper(
        //             id,
        //             algo
        //         )
        //         .then(response => {
        //             this.citations = response.data.similar_papers;
        //             this.nCitations = response.data.total_results;
        //             this.loading = false;
        //         })
        //         .catch(error => {
        //             this.loading = false;
        //             console.log(error);
        //         });
        // }
    }
};
</script>
<style>
.hidden_header {
    display: none;
}
</style>
