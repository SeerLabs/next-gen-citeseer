
<template>
    <!-- $ sudo sysctl fs.inotify.max_user_watches=524288
    $ sudo sysctl -p -->




    <div id="doc-view-layout">
        
        <b-container fluid>
            <!-- Search Box Row -->
            <b-row align-h="center">
                <b-col  cols="12"> 
                    <search-box/>
                </b-col>
            </b-row>
            <!-- Main Info Row -->
            <b-row>
                <b-col cols="5">
                    <h2>What papers cite this paper. . .</h2>
                </b-col>
                <b-col>
                    <b-button v-b-tooltip.hover title="You are seeing this page because the summary page is not indexed" size="sm" pill variant="outline-secondary">?</b-button>
                </b-col>
            </b-row>
            <b-row id="abstract" align-h="center">
                
                <b-col cols="9">
                    <h1>{{ title }}</h1>
                    <!-- <h5>{{ authors.join(', ')}}</h5> -->
                    <h5>{{ venue }} - {{ year }}</h5>
                    <br>
                    
                </b-col>
                
            </b-row>


            <b-row id ="citation-card" class="citation-card" align-h="center">
                <b-col cols="12">
                    <document-results-container 
                        :documents="documents"
                        :totalPageResults="totalPageResults"
                        :page="page"
                        :sortDropdown="sortDropdown"
                        v-model="sortBy"
                    />
                    <b-pagination
                        :total-rows="totalPageResults" 
                        v-model="page"
                        :per-page="pageSize"
                        @input="getCiting()"
                    />
                </b-col>
            </b-row>
            <!-- Citations Row -->
            <!-- <b-row id ="citation-card" class="citation-card" align-h="center">
                <b-col cols="12">
                    <citation-card id="citation-card" title="Citations" v-bind:doi="doi" v-bind:ncitation="nCitation"/>
                </b-col>
            </b-row> -->
            
        </b-container>    
    </div>
</template>

<script>
    import SearchBox from '~/components/SearchBox.vue'
    import CitationCard from '~/components/DocumentView/CitationCard.vue'
    import BaseCard from '~/components/Base/BaseCard.vue'
    import ShowCitingService from "~/api/ShowCitingService"
    import DocumentResultsList from "~/components/DocumentResults/DocumentResultsList.vue"
    import DocumentResultsContainer from "~/components/DocumentResults/DocumentResultsContainer.vue"
    export default {
        components: {
            SearchBox,
            CitationCard,
            BaseCard,
            DocumentResultsList,
            ShowCitingService,
            DocumentResultsContainer
        },
        
        data (){
            return {
                readMoreToggle: false,
                title : "", 
                year : 0,
                authors : [],
                venue : "",
                abstract : "",
                nCitation : "",
                totalPageResults: 1000,
                documents: [],
                sortBy: 'yearAsc',
                sortDropdown: {
                'citCount': {'displayName': 'Citation Count', 'sortByKey': 'citCount'},
                'yearAsc': {'displayName': 'Year (Ascending)', 'sortByKey': 'yearAsc'},
                'yearDesc': {'displayName': 'Year (Descending)', 'sortByKey': 'yearDesc'},
                },
                totalPageResults: 0,
                pageSize: 10,
                page: 1,
            }
        },
        mounted(){
            this.getCiting(),
            console.log("API IS BEING CALLED")
        },
        methods: {
            getCiting() {
                 
               
                ShowCitingService.getShowCiting(this.$route.params.id, this.page, this.pageSize, this.sortBy).then(response=>(
                    this.title = response.data.cluster.ctitle, 
                    this.year = response.data.cluster.cyear,
                    this.authors = response.data.cluster.cauthors,
                    this.venue = response.data.cluster.cvenue,

                    this.documents = response.data.papers,
                    this.totalPageResults = response.data.total_results,
                    console.log("id: " + this.$route.params.id),
                    console.log("page: " + this.page),
                    console.log("sort: " + this.sortBy)

                ))
            },
            alert() {
                window.alert("You are seeing this page because the summary page is not indexed.")
            }
        },
        watch: {
            sortBy: function() {
                this.getCiting()
            }
        },
        // async fetch() {
        //     const { data } = await ShowCitingService.getShowCiting(this.$route.params.id, this.page, this.pageSize)
        //     this.title = response.data.cluster.ctitle, 
        //     this.year = response.data.cluster.cyear,
        //     this.authors = response.data.cluster.cauthors,
        //     this.venue = response.data.cluster.cvenue,

        //     this.documents = response.data.papers,
        //     this.totalPageResults = response.data.total_results,
        //     console.log("id: " + this.$route.params.id),
        //     console.log("page: " + this.page),
        //     console.log("sort: " + this.sortBy)
        // },
        
        layout: 'layout_default',
        
        
    }
</script>

<style>
#doc-view-layout{
    background: rgb(255, 255, 255);
}
#side-margine {

}
#abstract {
    margin-top: 4%;
    margin-bottom: 2%;
    background: #ffffff;
}
#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
}
.citation-card {
    margin-top: 3%;
    margin-bottom: 3%;
}
#pdf-btn {
    background: rgb(235, 0, 0);
    outline: transparent;
    border-color: transparent;
}
#toc {
    position: fixed;
    right: 5%;
    margin-top: 20%;
}
</style>
