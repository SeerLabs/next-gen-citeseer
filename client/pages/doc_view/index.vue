<template>
    <div id="doc-view-layout">
        
        <navbar/>

        <search-box id="side-margine"/>
        
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
        <div id="side-margine">
            <citation-card id="citation-card" title="Citations" ncitation="ncitation"/>
            <citation-card id="citation-card" title="Active Bibilography" ncitation="ncitation"/>
            <citation-card id="citation-card" title="Co-citations" ncitation="ncitation"/>
            <citation-card id="citation-card" title="Clustered Documents" ncitation="ncitation"/>
        </div>  
        
    </div>
</template>

<script>
    import Navbar from '~/components/Navbar.vue'
    import SearchBox from '~/components/SearchBox.vue'
    import CitationCard from '~/components/CitationCard.vue'

    export default {
        components: {
            Navbar,
            SearchBox,
            CitationCard
        }
    }
</script>

<style>
#doc-view-layout{
    background: rgb(236, 236, 236);
}
#side-margine {
    margin-left: 20%;
    margin-right: 20%;
  
}
#summary {
    margin-top: 2%;
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
    margin-top: 2%;
    margin-bottom: 2%;
}

</style>
