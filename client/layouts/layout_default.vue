<template>
    <div>
        <v-app v-cloak>
            <nav-bar />
            <v-main>
                <v-container id="page-container">
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
        NavBar,
        FooterBar
    },
    async mounted() {
      try {
        await this.$recaptcha.init()
      } catch (e) {
        // eslint-disable-next-line
        console.log(e);
      }
    }
};
</script>

<style>
#page-container {
    margin: auto auto;
    margin-bottom: 400px;
}

#app {
    text-align: left;
}

[v-cloak] {
    display: none;
}
</style>
