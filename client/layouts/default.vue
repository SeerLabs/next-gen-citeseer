<template>
    <div>
        <v-app v-cloak>
            <nav-bar />
            <v-main>
                    <v-alert
                      :value="displayNotification"
                      :type="notificationType"
                    >
                      {{ notificationText }}
                    </v-alert>
                    <math-deck-panel></math-deck-panel>
                    <nuxt v-if="!$slots.default" keep-alive  />
                    <slot />
            </v-main>
            <footer-bar></footer-bar>
        </v-app>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import NavBar from '~/components/Navigation/Navbar.vue';
import FooterBar from '~/components/Navigation/FooterBar.vue';
import MathDeckPanel from '~/components/MathDeck/MathDeckPanel.vue';


export default {
    name: 'LayoutDefault',
    components: {
        NavBar,
        FooterBar,
        MathDeckPanel
    },
    computed: {
      ...mapState([
        'displayNotification',
        'notificationText',
        'notificationType'
      ])
    },
    watch:{
    $route (to, from){
      if(!(to.name === "login")) {
        this.$store.commit('closeNotification')
      }
    }
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
#app {
    text-align: left;
    font-family: "Open Sans";
    position: 'relative';
}

h1, h2, h3, h4, h5 {
  font-family: "Bitter";
  font-weight: 600;
}

a {
  text-decoration: none;
}

[v-cloak] {
    display: none;
}
</style>
