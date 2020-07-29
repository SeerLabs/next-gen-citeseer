<template>
    <div>
        <v-app>
            <nav-bar />
            <v-main>
                <v-container>
                    <v-col id="page-container" cols="12">
                        <v-row>
                            <v-col id="search-box-container" cols="8">
                                <search-box v-model="searchQuery" />
                            </v-col>
                        </v-row>
                        <nuxt keep-alive />
                    </v-col>
                </v-container>
                <footer-bar />
            </v-main>
        </v-app>
    </div>
</template>

<script>
import NavBar from '~/components/Navigation/Navbar.vue';
import FooterBar from '~/components/Navigation/FooterBar.vue';
import SearchBox from '~/components/SearchBox.vue';

export default {
    components: {
        NavBar,
        FooterBar,
        SearchBox
    },
    data() {
        return {
            searchQuery: ''
        };
    }
};
</script>

<style>
#search-box-container {
    margin: 1.5em 0;
}
</style>
