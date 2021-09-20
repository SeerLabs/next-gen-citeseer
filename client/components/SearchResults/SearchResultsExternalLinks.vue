<template>
    <div id="search-results-external-links">
        <v-card :title="filter_title" outlined>
            <v-toolbar flat dense color="primary"><h5 class="secondary--text ma-0">Try your query at</h5></v-toolbar>
            <v-card-text>
                <v-container>
                <b-row rows="3">
                    <b-col cols="12">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/semantic.png" alt="Semantic Scholar" /></a>
                    </b-col>
                    <b-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/googlescholar_icon.png" alt="Google Scholar" /></a>
                    </b-col>
                    <b-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/microsoftacademicsearch_icon.jpg" alt="Semantic Scholar" /></a>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/google_icon.jpg" alt="Semantic Scholar" /></a>
                    </b-col>
                    <b-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon"  src="../../assets/img/bing_icon.jpg" alt="Semantic Scholar" /></a>
                    </b-col>
                    <b-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/dblp_icon.png" alt="Semantic Scholar" /></a>
                    </b-col>
                </b-row>
                </v-container>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
export default {
    name: 'SearchResultsExternalLinks',
    props: {
        query: {type: String}
    },
    data() {
        return {
            semantic_scholar_url: 'https://www.semanticscholar.org/search?q=' + this.query,
        };
    }
};
</script>

<style scoped>
#search-results-external-links {
    margin-bottom: 20px !important;
}
#icon {
    width:100%;
    max-width:50px;
}
</style>
