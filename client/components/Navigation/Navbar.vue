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
              <nuxt-link class="navbar-home-link" to="/myciteseer/profile"><v-btn>Profile</v-btn></nuxt-link>
              <v-btn class="navbar-home-link" @click="logoutUser">Logout</v-btn>
            </div>
            <div v-else>
              <nuxt-link class="navbar-home-link" to="/register"><v-btn>Register</v-btn></nuxt-link>
              <nuxt-link class="navbar-home-link" to="/login"><v-btn>Login</v-btn></nuxt-link>
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
        logout: 'auth/logout',
        showNotification: 'showNotification'
      }),

      logoutUser() {
          this.logout();
          this.$router.push("/login");
          this.showNotification({
            text: "Logged out successfully",
            type: "success"
        });
      }
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
