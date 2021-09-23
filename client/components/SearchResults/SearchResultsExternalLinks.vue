<template>
    <div id="search-results-external-links">
        <v-card :title="filter_title" outlined rounded=0>
            <v-toolbar flat dense color="primary"><h5 class="white--text ma-0">Try your query at</h5></v-toolbar>
            <v-card-text>
                <v-container>
                <v-row justify="center">
                    <v-col 
                        v-for="(site, index) in sites"
                        :key="index"
                        cols="4"
                        align="center"
                    >   
                        <a :href="site.url" target="_blank">
                            <img id="icon" :src="site.logo" :alt="site.name"/>
                        </a>
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
            sites: {
                'semantic' : {
                    name: 'Semantic Scholar',
                    url: 'https://www.semanticscholar.org/search?q=' + this.query,
                    logo: require('../../assets/img/semantic.png'),
                },
                'google_scholar' : {
                    name: 'Google Scholar',
                    url: 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C39&q=' + this.query,
                    logo: require('../../assets/img/google_scholar.png'),
                },
                'microsoft' : {
                    name: 'Microsoft Academic Research',
                    url: 'https://academic.microsoft.com/search?q=' + this.query,
                    logo: require('../../assets/img/microsoft_research.jpg'),
                },
                'google': {
                    name: 'Google',
                    url: 'https://www.google.com/search?q=' + this.query,
                    logo: require('../../assets/img/google.png'),
                },
                'dblp': {
                    name: 'dblp',
                    url: 'https://dblp.org/search?q=' + this.query,
                    logo: require('../../assets/img/dblp.png'),
                },
                'bing': {
                    name: 'Bing',
                    url: 'https://www.bing.com/search?q=' + this.query,
                    logo: require('../../assets/img/bing.png'),
                }
            },
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
