<template>
    <div class="overflow-auto">
        <citation-item id="citation-list" 
            v-for="citation in citations" v-bind:key="citation" 
                v-bind:title="citation.title"
                v-bind:year="citation.year"
                authors="[name, kname, sdname]"
                v-bind:abstract="citation.abstract"

            />
        
        <p class="mt-3">Current Page: {{ currentPage }}</p>
        <!-- <li id="citation-list" v-for="citation in citations" v-bind:key="citation">
            <document-results-item 
                v-bind:title="citation.title"
                v-bind:authors="citation.author"
                v-bind:year="citation.year"
                v-bind:abstract="citation.abstract"

            />
        </li> -->
        <!-- <b-table
            id="my-table"
            thead-class="hidden_header"
            :items="items"
            :per-page="perPage"
            :current-page="currentPage"
            small
        ></b-table> -->

        <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            @input="getCitationEntities(currentPage)"
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
                    type: String
                },
                perPage: 3,
                currentPage: 1,
                citations: []
                // citations: [
                //     {title: 'Place Holder For Paper Titile Here 1', author: "author 1", year: "year 1", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 2', author: "author 2", year: "year 2", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 3', author: "author 3", year: "year 3", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 4', author: "author 4", year: "year 4", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 5', author: "author 5", year: "year 5", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 6', author: "author 6", year: "year 6", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 7', author: "author 7", year: "year 7", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 8', author: "author 8", year: "year 8", abstract: "abstract - The objective of this paper is to ..."},
                //     {title: 'Place Holder For Paper Titile Here 9', author: "author 9", year: "year 9", abstract: "abstract - The objective of this paper is to ..."}
                // ]
            }
        },
        mounted(currentPage) {
            this.getCitationEntities(currentPage)
        },
        computed: {
            rows() {
                return this.citations.length
            }
        },
        methods: {
            getCitationEntities(currentPage){
                docViewService.getCitationsEntities("d0b9b55d-87b6-49e1-9d0b-4aa8f1b7a115")
                .then(response => (this.citations = response.data))
            }
        }
    }
</script>
<style>
.hidden_header {
  display: none;
}

</style>