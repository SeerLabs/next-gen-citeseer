<template>
    <div>
        <v-app v-cloak>
            <nav-bar />
            <v-main>
                <v-container>
                    <nuxt keep-alive />
                </v-container>
            </v-main>
            <footer-bar />
        </v-app>
    </div>
</template>

<script>
import NavBar from '~/components/Navigation/Navbar.vue';
import FooterBar from '~/components/Navigation/FooterBar.vue';

export default {
    name: 'LayoutDefault',
    components: {
        NavBar: NavBar,
        FooterBar: FooterBar
    }
};
</script>

<style>
#page-container {
    margin: auto;
}

#app {
    text-align: left;
}

[v-cloak] {
    display: none;
}
</style>
