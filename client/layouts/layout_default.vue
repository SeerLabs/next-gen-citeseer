<template>
    <div>
        <v-app v-cloak>
            <nav-bar />
            <v-main>
                <div id="bg-wrapper">
                    <v-container id="page-container">
                        <nuxt keep-alive />
                    </v-container>
                </div>
            </v-main>
            <footer-bar id="footer"/>
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
#bg-wrapper {
    background-image: url('../assets/img/bg_colored.png');
    background-size: cover;
    background-position: bottom;
    background-size: 100% 60%;
    height: 100%;
}

.v-btn {
    text-transform: none;
}

[v-cloak] {
    display: none;
}
</style>
