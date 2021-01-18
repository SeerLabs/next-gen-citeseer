<template>
    <div>
        <v-app v-cloak>
            <nav-bar />
            <v-main>
                <v-container>
                    <v-alert
                      :value="displayNotification"
                      :type="notificationType"
                    >
                      {{ notificationText }}
                    </v-alert>

                    <nuxt v-if="!$slots.default" keep-alive />
                    <slot />
                </v-container>
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
