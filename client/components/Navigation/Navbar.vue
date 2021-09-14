<template>
    <header>
        <v-app-bar id="navbar" color="primary" flat>
            <v-toolbar-title href="#">
                <nuxt-link :to="{ path: '/' }">
                    <v-btn text>CiteSeerX</v-btn>
                </nuxt-link>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <div v-if="loggedIn">
              <nuxt-link to="/myciteseer/profile"><v-btn text>Profile</v-btn></nuxt-link>
              <v-btn text @click="logoutUser">Logout</v-btn>
            </div>
            <div v-else>
              <nuxt-link to="/register"><v-btn>Register</v-btn></nuxt-link>
              <nuxt-link to="/login"><v-btn>Login</v-btn></nuxt-link>
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

</style>
