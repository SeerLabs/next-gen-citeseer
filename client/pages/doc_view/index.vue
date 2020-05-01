<template>
    <div id="doc-view-layout">
        
        <navbar/>
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
                    <!-- <h5>{{ authors}}}</h5> -->
                    <h5>{{ year }}</h5>
                    <br>
                    <p v-if="!readMoreToggle">
                        {{abstract.slice(0, 700)}} 
                        <b-button v-if="!readMoreToggle" @click="toggleReadMore()">
                            Read more...
                        </b-button>
                    <p v-else>
                        {{ abstract }}
                        <!-- <span v-show="readMoreToggle" v-html="abstract"></span> -->
                    </p>
                </b-col>
                <b-col cols="2">
                    <b-card>
                        <!-- PDF Button -->
                        <b-row>
                            <b-col><b-button squared id="pdf-btn" >View PDF</b-button></b-col>
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
            <b-row id="citation-card" align-h="center">
                <b-col cols="8">
                    <citation-card id="citation-card" title="Citations" ncitation="ncitation"/>
                </b-col>
            </b-row>
            
            <!-- Similar Articles Row -->
            <b-row id="citation-card" align-h="center">
                <b-col cols="8">
                    <citation-card id="citation-card" title="Similar Articles" ncitation="ncitation"/>
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
    import SearchBox from '~/components/SearchBox.vue'
    import CitationCard from '~/components/CitationCard.vue'
    import BaseCard from '~/components/Base/BaseCard.vue'
    import DocViewService from "~/api/DocViewService"
    export default {
        components: {
            Navbar,
            SearchBox,
            CitationCard,
            BaseCard
        },
        methods: {
            toggleReadMore : function(){
                this.readMoreFlag = true
            }
        },
        data (){
            return {
                title: "",
                year: "",
                authors: [],
                abstract: "",
                readMoreToggle: false
            }
        },
        mounted() {
            DocViewService.getPaperEntity("d0b9b55d-87b6-49e1-9d0b-4aa8f1b7a115")
                .then(response => (
                    this.title = response.data[0].title, 
                    this.year = response.data[0].year,
                    this.authors = response.data[0].authors,
                    this.abstract = response.data[0].abstract 
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
#citation-card {
    margin-top: 3%;
    margin-bottom: 3%;
}
#pdf-btn {
    background: rgb(235, 0, 0);
    outline: transparent;
    border-color: transparent;
}

</style>
