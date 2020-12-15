<template>
    <div>
    <div v-if="profile" id="homepage">
        <h1>MyCiteSeer</h1>

        <v-tabs v-model="tab" vertical>
          <v-tab>
            Profile
          </v-tab>
          <v-tab>
            Settings
          </v-tab>
        
        <v-tabs-items v-model="tab">
          <v-tab-item>
            <v-card flat>
              Profile
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              Settings
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        </v-tabs>
    </div>
    </div>
</template>

<script>
/* eslint-disable */
import { mapState } from 'vuex'
import authService from '~/api/AuthService'

export default {
    data() {
      return {
        tab: null,
        items: ['Profile', 'Settings'],
        profile: null
      }
    },
    computed: {
      ...mapState(['auth'])
    },
    created() {
      console.log(this.auth);
      console.log(this.auth.loggedIn)

      if (!this.auth.loggedIn) {
        console.log("Not logged in");
        this.$router.push("/login");
      }
      else {
        console.log("Logged in");
        authService.getUserProfile(this.auth.token)
        .then((response) => {
          console.log(response)
          this.profile = response.data;
        });
        console.log(this.profile)
      }
    },
    layout: 'layout_default'
};
</script>

<style>
#homepage {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin: 10% auto;
    width: 75vw;
}

#logo {
    width: 20em;
    margin-bottom: 1em;
}
</style>
