<template>
    <header>
        <v-app-bar id="navbar" color="primary" flat>
            <v-toolbar-title href="#">
                <nuxt-link :to="{ path: '/' }">
                    <img src="@/assets/img/logo_white.png" alt="CiteSeerX" width="150">
                </nuxt-link>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <div>
              <a 
                v-for="link in links" 
                :key="link.id" 
                :href="link.url" 
                target="_blank"
                class="link"
              >
                {{ link.title }}
              </a>
            </div>

            <!-- MyCiteSeerX functionalities was removed, need to be added back in.  -->
            <!-- <div v-if="loggedIn">
              <nuxt-link to="/myciteseer/profile" class="link">Profile</nuxt-link>
              <a @click=logoutUser>Logout</a>
            </div>
            <div v-else>
              <nuxt-link to="/register"><v-btn>Register</v-btn></nuxt-link>
              <nuxt-link to="/login"><v-btn>Login</v-btn></nuxt-link>
            </div> -->
        </v-app-bar>
    </header>
</template>


<script>
import { mapMutations } from 'vuex'

export default {
    data() {
      return {
        links: [
          {
            title: 'About',
            url: 'http://csxstatic.ist.psu.edu/home',
          },
          {
            title: 'Donate',
            url: 'http://www.givenow.psu.edu/CiteseerxFund',
          },
          {
            title: 'DMCA',
            url: 'https://www.psu.edu/copyright-information/',
          }
        ],
      }
    },
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
  .link {
    color: #ffff !important;
    margin-right: 3em;
  }
</style>
