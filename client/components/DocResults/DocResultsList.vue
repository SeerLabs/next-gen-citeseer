<template>
    <div class="document-results-list">
        <ul>
            <li v-for="item in documents" :key="item.id">
                <doc-results-item
                    class="document-results-item"
                    :doc-id="item.id"
                    :cluster-id="item.cluster_id"
                    :title="item.title"
                    :type="item.type"
                    :authors="item.authors"
                    :year="item.year"
                    :abstract="item.abstract"
                    :n-cited-by="item.n_cited_by"
                    :n-self-cites="item.n_self_cites"
                />
                
            </li>
        </ul>
    </div>
</template>

<script>
import DocResultsItem from './DocResultsItem';

export default {
    name: 'DocResultsList',
    components: {
        DocResultsItem
    },
    props: {
        documents: { type: Array, default: null }
    }
};
</script>

<style scoped>
.document-results-list {
    margin: 1.5em 0 1em 0;
    padding: 0;
}

.document-results-list ul {
    list-style: none;
    padding-left: 0;
}

.document-results-item {
    margin: 0.5em 0;
}
</style>
