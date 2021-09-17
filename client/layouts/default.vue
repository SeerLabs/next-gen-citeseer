<template>
    <div>
        <v-app v-cloak>
            <nav-bar />
            <v-main id="page-container">
                    <v-alert
                      :value="displayNotification"
                      :type="notificationType"
                    >
                      {{ notificationText }}
                    </v-alert>

                    <nuxt v-if="!$slots.default" keep-alive  />
                    <slot />
            </v-main>
            <footer-bar />
        </v-app>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import NavBar from '~/components/Navigation/Navbar.vue';
import FooterBar from '~/components/Navigation/FooterBar.vue';


export default {
    name: 'LayoutDefault',
    components: {
        NavBar,
        FooterBar
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
#page-container {
  margin-bottom: 400px;
}


#app {
    text-align: left;
}

[v-cloak] {
    display: none;
}
</style>
