<template>
    <div class="overflow-auto">
        <citation-item id="citation-list" 
            v-for="citation in citations" v-bind:key="citation" 
                v-bind:title="citation.title"
                v-bind:year="citation.year"
                v-bind:authors="citation.authors"
                v-bind:venue="citation.venue"
                

            />
        
        <p class="mt-3">Current Page: {{ currentPage }}</p>

        <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            @input="getCitationEntities()"
        ></b-pagination>
    </div>
</template>

<script>
    import DocumentResultsItem from "~/components/DocumentResults/DocumentResultsItem.vue"
    import docViewService from "~/api/DocViewService"
    import CitationItem from "./CitationItem"
    export default {
        name: 'CitationCard',
        components: {
            DocumentResultsItem,
            CitationItem
        },
        data() {
            return {
                props: {
                    doi: String, 
                    type: String,
                    
                },
                perPage: 3,
                currentPage: 1,
                citations: []
            }
        },
        mounted(currentPage) {
            this.getCitationEntities()
        },
        computed: {
            rows() {
                return this.citations.length
            }
        },
        methods: {
            getCitationEntities(){
                if (true) {
                    docViewService.getCitationsEntities(this.$route.params.id, this.currentPage)
                        .then(response => (this.citations = response.data.citations))
                }
                
                
            }
        }
    }
</script>
<style>
.hidden_header {
  display: none;
}

</style>