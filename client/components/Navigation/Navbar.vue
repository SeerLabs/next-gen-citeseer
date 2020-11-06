<template>
    <header>
        <v-app-bar id="navbar" dark>
            <v-toolbar-title href="#">
                <nuxt-link class="navbar-home-link" :to="{ path: '/' }">
                    CiteSeerX
                </nuxt-link>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <div v-if="isAuthenticated">
              {{ loggedInUser.username }}
            </div>
            <div v-else>
              <nuxt-link class="navbar-home-link" to="/register">Register</nuxt-link>
              <nuxt-link class="navbar-home-link" to="/login">Login</nuxt-link>
            </div>
        </v-app-bar>
    </header>
</template>


<script>
import { mapGetters } from 'vuex'

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'loggedInUser'])
  }
}
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
