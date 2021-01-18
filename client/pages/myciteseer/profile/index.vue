<template>
    <div>
    <div v-if="profile" id="profile">
        <div class="text-h2 mb-10 text-center">MyCiteSeer</div>

        <v-tabs v-model="tab" vertical>
          <v-tab>
            Profile
          </v-tab>
          <v-tab>
            Settings
          </v-tab>
        
        <v-tabs-items v-model="tab" class="ml-10">
          <v-tab-item>

            <v-card flat>
              <v-card-title>
                Liked Papers 
              </v-card-title>

              <v-card-text>
                <doc-results-list
                  v-if="likedPapers.length"
                  class="profile-documents-list"
                  :documents="likedPapers" 
                />
                <div v-else class="text-body1 filler-text">
                  No liked papers added
                </div>
              </v-card-text>
            </v-card>

            <v-card flat>
              <v-card-title>
                Monitered Papers 
              </v-card-title>

              <v-card-text>
                <doc-results-list 
                  v-if="moniteredPapers.length" 
                  class="profile-documents-list"
                  :documents="moniteredPapers" 
                />
                <div v-else class="text-body1 filler-text">
                  No monitered papers added
                </div>
              </v-card-text>
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
import docViewService from '~/api/DocViewService'

import DocResultsList from '~/components/DocResults/DocResultsList'

export default {
    components: { DocResultsList },
    data() {
      return {
        tab: null,
        items: ['Profile', 'Settings'],
        profile: null,
        likedPapers: [],
        moniteredPapers: [],
      }
    },
    computed: {
      ...mapState(['auth'])
    },
    methods: {
      
    },
    mounted() {

      if (!this.auth.loggedIn) {
        this.$router.push("/login");
      }
      else {
        authService.getUserProfile(this.auth.token)
        .then(async (response) => {
          this.profile = response.data;

          this.likedPapers = await docViewService.getPaperswithPaperIds(this.profile.liked_papers)
          this.moniteredPapers = await docViewService.getPaperswithPaperIds(this.profile.monitered_papers)

          console.log(this.likedPapers);
          console.log(this.moniteredPapers);
        });
        console.log(this.profile)
      }
    },
};
</script>

<style scoped>
#profile {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    width: 75vw;
    margin: auto;
}

.profile-documents-list {
  background: lightgray;
  padding: 1rem;
}


.filler-text {
  font-size: 1.25rem;
  font-weight: 500;
  text-align: center;
  padding: 2rem;
}
</style>
