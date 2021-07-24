<template>
    
        <v-container id="homepage">
            <img id="logo" src="@/assets/img/csx_logo.png" alt="CiteSeerX" />
            <h4 id="subtitle">Search across over 10,000,000 documents, journals, and papers</h4>
            <search-box id="search-bar"/>
            <v-row>
                <v-col>
                    <v-checkbox label="Include Citations" class="pa-t-3 ma-0"></v-checkbox>
                </v-col>
                <v-spacer></v-spacer>
                <v-col>
                    <v-btn 
                        id="adv-search-btn" 
                        text 
                        href="#"
                        class="secondary--text text--darken-5"
                    >
                        Advanced Search
                    </v-btn>
                </v-col>
            </v-row>
            <v-row justify="center" class="pt-10">
                <nuxt-link :to="{ path: '/' }">Want to submit a document?</nuxt-link>
                <v-divider id="divider" vertical class="mx-5 primary lighten-5"></v-divider>
                <nuxt-link :to="{ path: '/' }">FAQ</nuxt-link>
            </v-row>
            <v-row justify="center" align="center" class="pt-5">
                Powered by <img id="elastic-search" src="@/assets/img/logo-elastic-horizontal-color.svg" alt="Elastic Search"/>
            </v-row>
            
        </v-container>

</template>

<script>
import SearchBox from '~/components/SearchBox.vue';
export default {
    components: {
        SearchBox
    },
    layout: 'layout_default',
};
</script>

<style>

#homepage {
    text-align: center;
    margin-top: 10%;
}

#logo {
    width: 25em;
}

#subtitle {
    color: var(--v-secondary-darken5);
    font-size: 1.5em;
    font-weight: 200;
}

#search-bar {
    margin-top: 4em;
}

#adv-search-btn {
   transform: translateX(5em);
}   

#elastic-search {
    width: 8em;
    margin: 2em 10px;
}

#divider {
    border-width: 0.8px;
    
}

</style>
