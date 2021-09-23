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
                    :collection-names="collectionNames"
                />
                
            </li>
        </ul>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import DocResultsItem from './DocResultsItem';
export default {
    name: 'DocResultsList',
    components: {
        DocResultsItem
    },
    props: {
        documents: { type: Array, default: null }
    },
    data(){
        return{
            collectionNames: [],
        };
    },
    computed: {
        ...mapState(['auth']),    
    },
    beforeMount() {
      if (this.auth.loggedIn) {
        this.getUserProfile({token: this.auth.token})
        .then((profile) => {
          for (const i in profile.collections){
            this.collectionNames.push(profile.collections[i].collection_name)
          }
        })
      }
    },
    methods:{

        ...mapActions(['getUserProfile'])
    }
};
</script>

<style scoped>

.document-results-list ul {
    list-style: none;
    padding-left: 0;
}

.document-results-item {
    margin: 0.5em 0;
}

/* remove top margin of the first child */
.document-results-item:first-child {
    margin-top: 0;
}
</style>
