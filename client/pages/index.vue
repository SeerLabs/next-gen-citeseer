<template>
    <div id="homepage">
     <v-container class="mt-16">
        <img id="logo" src="@/assets/img/csx_logo.png" alt="CiteSeerX"/>
        <h4 id="subtitle" class="mt-3">Search across over 10,000,000 documents, journals, and papers</h4>

        <v-row justify="center" class="mt-10">
            <v-col md="10">
                <search-box id="search-bar"/>
            </v-col>   
        </v-row>  

        <v-row justify="center" class="pt-10">
            <nuxt-link :to="{ path: '/' }">Want to submit a document?</nuxt-link>
            <v-divider id="divider" vertical class="mx-5 primary lighten-5"></v-divider>
            <nuxt-link :to="{ path: '/' }">FAQ</nuxt-link>
        </v-row>
        <v-row justify="center" align="center" class="pt-3">
            Powered by <img id="elastic-search" src="@/assets/img/logo-elastic-horizontal-color.svg" alt="Elastic Search"/>
        </v-row>
            
        </v-container>
        </div>
</template>

<script>
import SearchBox from '~/components/SearchBox.vue';

export default {
    components: {
        SearchBox
    },
};
</script>

<style scoped>
#homepage {
    text-align: center;
    background-image: url("../assets/img/bg_colored.png");
    background-size: cover;
    background-position: bottom;
    background-size: 100% 80%;
    height: 100%;
}

#logo {
    width: 28em;
}

#subtitle {
    color: var(--v-secondary-base);
    font-family: "Open Sans";
    font-size: 1.8em;
    font-weight: 400;
}

#elastic-search {
    width: 8em;
    margin: 2em 10px;
}

#divider {
    border-width: 0.8px;
    
}
</style>
