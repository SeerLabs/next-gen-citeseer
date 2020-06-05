<template>
    <div id="doc-view-layout">
        
        <navbar/>
        <b-card id="toc">
            <b-row>
                <b-col><h6 v-on:click="scroll('citation-card')" >Citation</h6></b-col>
            </b-row>
            <br>
            <b-row>
                <b-col><h6 v-on:click="scroll('similar-article-card')" >Similar Article</h6></b-col>
            </b-row>
            <br>
            <b-row>
                <b-col><h6 v-on:click="scroll('ver-history-card')" >Version History</h6></b-col>
            </b-row>
            
        </b-card>
        <b-container fluid>
            <!-- Search Box Row -->
            <b-row align-h="center">
                <b-col  cols="7"> 
                    <search-box/>
                </b-col>
            </b-row>
            <!-- Main Info Row -->
            <b-row id="abstract" align-h="center">
                <b-col cols="6">
                    <h1>{{ title }}</h1>
                    <h5>{{ authors.join(', ')}}</h5>
                    <h5>{{ venue }} - {{ year }}</h5>
                    <br>
                    <p v-if="!readMoreToggle">
                        {{abstract.slice(0, 700)}} 
                        <a href="">
                            Read more...
                        </a>
                    <p v-else>
                        {{ abstract }}
                        <!-- <span v-show="readMoreToggle" v-html="abstract"></span> -->
                    </p>
                </b-col>
                <b-col cols="2">
                    <b-card>
                        <!-- PDF Button -->
                        <b-row>
                            <b-col><b-button squared id="pdf-btn" v-bind:to="pdfURL">View PDF</b-button></b-col>

                        </b-row>
                        
                        <!-- Download Links Drop Down -->
                        <b-row>
                            <b-dropdown id="download-links-dropdown" text="Download Links" variant="outline-secondary" class="m-md-2" size="sm">
                                <b-dropdown-item>Link 1</b-dropdown-item>
                                <b-dropdown-item>Link 2</b-dropdown-item>
                                <b-dropdown-item>Link 3</b-dropdown-item>
                            </b-dropdown>
                        </b-row>
                        <b-row >
                            <b-col> <h6>Cite This</h6> </b-col>
                        </b-row>
                        <b-row>
                            <b-col><h6>Save</h6></b-col>
                        </b-row>
                        <b-row>
                            <b-col><h6>Add to Collection</h6></b-col>
                        </b-row>
                        <b-row>
                            <b-col><h6>Add to MetaCart</h6></b-col>
                        </b-row>
                        <b-row>
                            <b-col><h6>Correct Errors</h6></b-col>
                        </b-row>
                       
                        
                        
                        
                        
                    </b-card>
                </b-col>
            </b-row>

            <!-- Citations Row -->
            <b-row id ="citation-card" class="citation-card" align-h="center">
                <b-col cols="8">
                    <citation-card id="citation-card" title="Citations" v-bind:ncitation="nCitation"/>
                </b-col>
            </b-row>
            
            <!-- Similar Articles Row -->
            <b-row id ="similar-article-card" class="citation-card" align-h="center">
                <b-col cols="8">
                    <citation-card id="citation-card" title="Similar Articles" ncitation=""/>
                </b-col>
            </b-row>

            <!-- Similar Articles Row -->
            <b-row id="ver-history-card" class="citation-card" align-h="center">
                <b-col cols="8">
                    <version-history-card title="Version History"/>
                </b-col>
            </b-row>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <br>
            <!-- Similar Articles Row -->
            <b-row class="citation-card" align-h="center">
                <b-col cols="8">
                    <document-results-list :documents="documents" :totalPageResults="totalPageResults"/>
                </b-col>
            </b-row>

            <!--             
            <div id = "summary">
                <div id = "summary-text">
                    <h1>Place Holder For Title</h1>
                    <h5>Auther Name</h5>
                    <h5>Vanue - Year</h5>
                    <br>
                    <p> Place  holder for abstract ... Es ging durch so schnelle Verrenkungen, dass der kleine Bär gezwungen war, kleine Bär gezwungen war,seinen Griff 
                        so oft zu ändern, dass er . seine untersten Rippen stie, dieser Punkt wurde für ihn einen in der Dunkelheit verwirrt Moment später von dem Tier selbst entschieden, wurde und für sein Leben nicht sagen konnte, ob er die Schafe mit der rechten Seite nach oben 
                        oder nach oben hielt Nieder. Aber dieser Punkt wurde für ihn einen Moment später von dem Tier selbst entschieden, das mit einer plötzlichen Drehung 
                        seine Hörner so fest in seine untersten Rippen stieß, dass er vor Wut und Ekel grunzte....
                    </p>
                </div>
            </div>
            <div>
                <citation-card id="citation-card" title="Citations" ncitation="ncitation"/>
                <citation-card id="citation-card" title="Active Bibilography" ncitation="ncitation"/>
                <citation-card id="citation-card" title="Co-citations" ncitation="ncitation"/>
                <citation-card id="citation-card" title="Clustered Documents" ncitation="ncitation"/>
            </div>   -->
        </b-container>    
    </div>
</template>

<script>
    import Navbar from '~/components/Navbar.vue'
    import TableOfContent from '~/components/DocumentView/TableOfContent.vue'
    import SearchBox from '~/components/SearchBox.vue'
    import CitationCard from '~/components/DocumentView/CitationCard.vue'
    import BaseCard from '~/components/Base/BaseCard.vue'
    import DocViewService from "~/api/DocViewService"
    import DocumentResultsList from "~/components/DocumentResults/DocumentResultsList.vue"
    import VersionHistoryCard from "~/components/DocumentView/VersionHistoryCard.vue"

    export default {
        components: {
            Navbar,
            TableOfContent,
            SearchBox,
            CitationCard,
            BaseCard,
            DocumentResultsList,
            VersionHistoryCard,
        },
        methods: {
            toggleReadMore : function(){
                this.readMoreFlag = true
            },
            scroll(id) {
              document.getElementById(id).scrollIntoView();
            }
        },
        data (){
            return {
                pdfURL: "/pdf/",
                title: "",
                year: "",
                authors: [],
                venue: "",
                abstract: "",
                nCitation: " Citations",
                readMoreToggle: false,

                 documents: [
              {'title': 'Document Title', 'type': 'DOCUMENT', 'authors': 'Abcdefg Lastname',
              'year': '2018', 'abstract': 'Lorem ipsum', 'numCitations': 20},
              {'title': 'ABCDEFG', 'type': 'DOCUMENT', 'authors': 'Hijklmno Pqrstuv',
              'year': '2020', 'abstract': 'Lorem ipsum', 'numCitations': 3},
              {'title': 'EFGHIJK', 'type': 'CITATION', 'authors': 'Firstname Lastname',
              'year': '2021', 'abstract': 'Lorem ipsum', 'numCitations': 30}
            ],
            totalPageResults: 1000
            }
        },
        mounted() {
            this.pdfURL += this.$route.params.id, 
            DocViewService.getPaperEntity(this.$route.params.id)
                .then(response => (
                    this.title = response.data.paper.title, 
                    this.year = response.data.paper.year,
                    this.authors = response.data.paper.authors,
                    this.venue = response.data.paper.venue,
                    this.abstract = response.data.paper.abstract,
                    this.nCitation = response.data.paper.n_citation + this.nCitation
                    ))
        }
        
        
    }
</script>

<style>
#doc-view-layout{
    background: rgb(255, 255, 255);
}
#side-margine {
    margin-left: 20%;
    margin-right: 20%;
  
}
#abstract {
    margin-top: 4%;
    margin-bottom: 2%;
    background: #ffffff;
}
#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
    margin-left: 20%;
    margin-right: 20%;
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
