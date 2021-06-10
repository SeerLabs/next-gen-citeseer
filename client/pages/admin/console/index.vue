<template>
    <div>
    <div v-if="username" id="profile">
        <div class="text-h2 mb-10 text-center">Admin Console</div>

        <v-tabs v-model="activeTabClass" vertical>
          <v-tab
            v-for="n in tabClasses"
            :key="n.id" 
          >
            {{ n.text }}
          </v-tab>
        
          <!-- <v-tabs-items v-model="tab" class="ml-10"> -->
            <v-tab-item v-for="(n, index) in tabClasses" :key="n.id">

              <v-card v-if="activeTabClass === 0" v-model="activeTab[index]" flat>
                <!-- <v-card-title>
                  Liked Papers 
                </v-card-title> -->
                <v-col class="text-h3 mb-10">MetaData Correction Requests</v-col>
                <!-- <div v-for="(c_meta, index) in correctMetadatas" :key="index"> -->
                   
                  <doc-results-list
                    v-if="correctMetadatas.length"
                    class="profile-documents-list"
                    :metadata-requests="correctMetadatas"
                    :papers="papers"
                  />
                  <div v-else class="text-body1 filler-text">
                    No Metadata Correction Request
                  </div>
                <!-- </div> -->
              </v-card>
              <v-card v-if="activeTabClass === 1" v-model="activeTab[index]" flat>
                <!-- <v-card-title>
                  Liked Papers 
                </v-card-title> -->
                <v-col class="text-h3 mb-10">MetaData Correction Archive</v-col>
                <!-- <div v-for="(c_meta, index) in correctMetadatas" :key="index"> -->
                   
                  <archived-res-list
                    v-if="editArchived.length"
                    class="profile-documents-list"
                    :metadata-requests="editArchived"
                    :papers="papersArchived"
                  />
                  <div v-else class="text-body1 filler-text">
                    No Metadata Correction Request
                  </div>
                <!-- </div> -->
              </v-card>
            </v-tab-item>
            
        </v-tabs>
    </div>
    </div>
</template>

<script>
/* eslint-disable */
import { mapState } from 'vuex'
import authService from '~/api/AuthService'
import DocViewService from '~/api/DocViewService'

import DocResultsList from '~/components/Admin/CorrectMetaDocResult'
import ArchivedResList from '~/components/Admin/EditArchivedResult'
export default {
    components: { DocResultsList, ArchivedResList },
    
    data() {
      return {
        activeTabClass: "1",
        tabClasses: [{id: 1, text: 'Metadata Correction Requests'},{id: 2, text: 'Metadata Correction Archive'},],
        username: null,
        activeTab: [],
        correctMetadatas: [],
        editArchived: [],
        papersArchived: [],
        papers: [],

      }
    },
    computed: {
      ...mapState(['admin_auth'])
    },
    methods: {

    },
    beforeMount() {
      if (!this.admin_auth.loggedIn) {
        this.$router.push("/admin/login");
      }
      else {
        this.username = this.admin_auth.username
        authService.get_edit_requests(this.admin_auth.token)
        .then((async (response) => {
            this.correctMetadatas = response.data;
            console.log("meta:")
            console.log(this.correctMetadatas)
            for (const i in this.correctMetadatas){
              let paper = await DocViewService.getPaperWithPaperId(this.correctMetadatas[i].user_request.paper_id)
              this.papers.push(paper.data.paper)
       
            }
            
            console.log("papes:")
            console.log(this.papers)
        }))

        authService.get_edit_archived(this.admin_auth.token)
        .then((async (response) => {
            this.editArchived = response.data;
            console.log("arch:")
            console.log(this.editArchived)
            for (const i in this.editArchived){
              let paper = await DocViewService.getPaperWithPaperId(this.editArchived[i].user_request.paper_id)
              this.papersArchived.push(paper.data.paper)
       
            }
            console.log("arch paper:")
            console.log(this.papersArchived)
        }))
        
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
  background: #435374;
  padding: 1rem;
}


.filler-text {
  font-size: 1.25rem;
  font-weight: 500;
  text-align: center;
  padding: 2rem;
}

.c_dropdown:after {
  content: '\2807';
  font-size: 2rem;
  }
</style>
