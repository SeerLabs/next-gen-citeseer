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
        </div>
    </div>
</template>

<script>
import CitationItem from './CitationItem';

export default {
    name: 'CitationList',
    components: {
        CitationItem
    },
    props: {
        docId: { type: String, default: '' },
        cid: { type: String, default: '' },
        doi: { type: String, default: '' },
        title: { type: String, default: '' },
        citations: {type:Array, default: null},
        nCitations: { type: Number, default: 0},
        loading: {type: Boolean, default: false}
    },
};
</script>
<style>
.hidden_header {
    display: none;
}
</style>
