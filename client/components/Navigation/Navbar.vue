<template>
    <header>
        <v-app-bar id="navbar" dark>
            <v-toolbar-title href="#">
                <nuxt-link class="navbar-home-link" :to="{ path: '/' }">
                    CiteSeerX
                </nuxt-link>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <div v-if="loggedIn">
              <nuxt-link class="navbar-home-link" to="/myciteseer/profile">{{ user.username }}</nuxt-link>
              <v-btn class="navbar-home-link" @click="logout">Logout</v-btn>
            </div>
            <div v-else>
              <nuxt-link class="navbar-home-link" to="/register">Register</nuxt-link>
              <nuxt-link class="navbar-home-link" to="/login">Login</nuxt-link>
            </div>
        </v-app-bar>
    </header>
</template>


<script>
import { mapMutations } from 'vuex'

export default {
    computed: {
      loggedIn() {
        return this.$store.state.auth.loggedIn
      },
      user() {
        return this.$store.state.auth.user
      }
    },
    methods: {
      ...mapMutations({
        logout: 'auth/logout'
      })
    }
};

</script>

<style scoped>
header {
    margin-bottom: 1.5em;
}

.navbar-home-link {
    color: white;
    text-decoration: none;
    margin-right: 1.em;
}
</style>
