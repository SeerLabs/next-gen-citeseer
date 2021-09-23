<template>
    <div id="search-results-external-links">
        <v-card :title="filter_title" outlined>
            <v-toolbar flat dense color="primary"><h5 class="white--text ma-0">Try your query at</h5></v-toolbar>
            <v-card-text>
                <v-container>
                <v-row rows="3" justify="center">
                    <v-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/semantic.png" alt="Semantic Scholar" /></a>
                    </v-col>
                    <v-col cols="3">
                        <a :href="google_scholar_url"> <img id="icon" src="../../assets/img/googlescholar_icon.png" alt="Google Scholar" /></a>
                    </v-col>
                    <v-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/microsoftacademicsearch_icon.jpg" alt="Semantic Scholar" /></a>
                    </v-col>
                </v-row>
                <v-row justify="center">
                    <v-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/google_icon.png" alt="Semantic Scholar" /></a>
                    </v-col>
                    <v-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon"  src="../../assets/img/bing_icon.jpg" alt="Semantic Scholar" /></a>
                    </v-col>
                    <v-col cols="3">
                        <a :href="semantic_scholar_url"> <img id="icon" src="../../assets/img/dblp_icon.png" alt="Semantic Scholar" /></a>
                    </v-col>
                </v-row>
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
            google_scholar_url: 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C39&q=' + this.query,
            microsoft_research_url: 'https://academic.microsoft.com/search?q=' + this.query,
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
