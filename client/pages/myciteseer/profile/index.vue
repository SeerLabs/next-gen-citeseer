<template>
    <div>
    <div v-if="profile" id="profile">
        <div class="text-h2 mb-10 text-center">MyCiteSeer</div>

        <v-tabs v-model="activeTabClass" vertical>
          <v-tab
            v-for="n in tabClasses"
            :key="n.id" 
          >
            {{ n.text }}
          </v-tab>
        
            <v-tab-item v-for="(n, index) in tabClasses" :key="n.id">

              <v-card v-if="activeTabClass === 0" v-model="activeTab[index]" flat>

                <v-col class="text-h3 mb-10">Liked Papers</v-col>
                <v-card-text>
                  <doc-results-list
                    v-if="likedPapers.length"
                    class="profile-documents-list"
                    :documents="likedPapers" 
                    @remove-paper="removeLikedPaper"
                  />
                  <div v-else class="text-body1 filler-text">
                    No liked papers added
                  </div>
                </v-card-text>
              </v-card>

              <v-card v-if="activeTabClass === 1" v-model="activeTab[index]" flat>

                <v-col class="text-h3 mb-10">Monitered Papers</v-col>
                <v-card-text>
                  <doc-results-list 
                    v-if="moniteredPapers.length" 
                    class="profile-documents-list"
                    :documents="moniteredPapers" 
                    @remove-paper="removeMoniteredPaper"
                  />
                  <div v-else class="text-body1 filler-text">
                    No monitered papers added
                  </div>
                </v-card-text>
              </v-card>
              
              <v-card v-if="activeTabClass === 2" v-model="activeTab[index]" flat>
                <v-col class="text-h3 mb-10">Collections</v-col>
                <v-tabs v-if="activeTabClass === 2" v-model="activeTab[index]" vertical>
                
                <v-tab
                  v-for="(n, c_index) in collections"
                  :key="n.name" 
                >
                  <v-col cols="11">{{ n.name }} </v-col>
                  <v-col cols="1"> 
                      <v-menu offset-y>
                        <template v-slot:activator="{ on, attrs }">
                          <div class="c_dropdown"
                            v-bind="attrs"
                            v-on="on"
                          >
                          </div>
                        </template>
                        <v-list>
                          <v-list-item>
                            <v-dialog
                                v-model="c_rename_dialog"
                                width="400"
                              >
                                <template v-slot:activator="{ on, attrs }">
                                  <div
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="rename_temp = n.name"
                                  >
                                    Rename
                                  </div>
                                </template>

                                <v-card>
                                  <v-card-title >
                                    Rename Collection
                                  </v-card-title>
                                <v-card-text>
                                <v-text-field
                                    v-model="rename_temp"
                                    label="Collection Name"
                                ></v-text-field>
                                </v-card-text>

                                  <v-divider></v-divider>

                                  <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn
                                      @click="renameCollection(c_index)"
                                    >
                                      Rename
                                    </v-btn>
                                    <v-btn
                                      color="primary"
                                      @click="c_rename_dialog = false"
                                    >
                                      Cancel
                                    </v-btn>
                                  </v-card-actions>
                                </v-card>
                              </v-dialog>
                          </v-list-item>




                          <v-list-item>
                            <v-dialog
                                v-model="c_delete_dialog"
                                width="400"
                              >
                                <template v-slot:activator="{ on, attrs }">
                                  <div
                                    v-bind="attrs"
                                    v-on="on"
                                  >
                                    Delete
                                  </div>
                                </template>

                                <v-card>
                                <v-card-text>
                                <h3>Are you sure you want to delete the 
                                    collection: {{ n.name }}?</h3>
                                </v-card-text>

                                  <v-divider></v-divider>

                                  <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn
                                      color="error"
                                      @click="deleteACollection(c_index)"
                                    >
                                      Delete
                                    </v-btn>
                                    <v-btn
                                      color="primary"
                                      @click="c_delete_dialog = false"
                                    >
                                      Cancel
                                    </v-btn>
                                  </v-card-actions>
                                </v-card>
                              </v-dialog>
                          </v-list-item>
                        </v-list>
                      </v-menu>  
                  </v-col>
                </v-tab>
                <v-tab-item v-for="(n, c_index) in collections" :key="n.name">
                  <v-card-text>
                    <doc-results-list
                      v-if="n.papers.length"
                      class="profile-documents-list"
                      :documents="n.papers" 
                      @remove-paper="removeCollectionPaper(c_index, $event)"
                    />
                    <div v-else class="text-body1 filler-text">
                      No collection papers added
                    </div>
                  </v-card-text>
                </v-tab-item>
          
              </v-tabs>
              </v-card>
              <v-card v-if="activeTabClass === 3" v-model="activeTab[index]" flat>
                <v-col class="text-h3 mb-10">Profile Information</v-col>
                <v-layout column>
                  <v-card flat>
                    <v-card-text>
                      <v-row>
                        <v-col cols="2">
                          Password
                        </v-col>
                        <v-col cols="4">
                          <v-btn @click="sendResetPasswordEmail()">
                            Send Password Reset Email
                          </v-btn>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="2">
                          Full Name
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.full_name"></v-text-field>
                        </v-col>
                      </v-row>
                      
                      <v-row>
                        <v-col cols="2">
                          Email
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.email"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Organization
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.organization"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Department
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.department"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Web Page
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.web_page"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          State
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.state"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Country
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="profile.country"></v-text-field>
                        </v-col>
                      </v-row>

                      
                      
                      <v-card-actions>
                        <v-btn :loading="loading" @click.native="update">
                            <v-icon left dark>check</v-icon>
                            Update Profile Information
                        </v-btn>
                      </v-card-actions>
                      
                      
                    </v-card-text>
                    
                  </v-card>
                </v-layout>
              </v-card>
            </v-tab-item>
        </v-tabs>
    </div>
    </div>
</template>

<script>
/* eslint-disable */
import { mapState, mapActions } from 'vuex'


import DocResultsList from '~/components/MyCiteSeer/MCSDocResults'

export default {
    components: { DocResultsList },
    data() {
      return {
        activeTabClass: "1",
        tabClasses: [{id: 1, text: 'Liked Papers'},{id:2, text:'Monitored Papers'}, {id:3, text:'Collections'}, {id:4, text:'Profile Info'}],
        profile: null,
        likedPapers: [],
        moniteredPapers: [],
        collections: [],
        activeTab: [],
        c_dropdown: [ {title: 'Rename'}, {title: 'Delete'}],
        c_delete_dialog: false,
        c_rename_dialog: false,
        rename_temp: ""

      }
    },
    computed: {
      ...mapState(['auth'])
    },
    methods: {
      ...mapActions(['sendResetPasswordEmail','deleteLikedPaper', 'deleteMoniteredPaper', 'deletePaperFromCollection', 'deleteACollection', 'renameCollection', 'getUserProfile', 
      'getPaperswithPaperIds']),
      sendResetPasswordEmail(){
        this.sendPasswordResetEmail({email: this.profile.email})
      },
      removeLikedPaper(index){
        this.deleteLikedPaper({token: this.auth.token, pid: this.likedPapers[index].id});
        this.likedPapers.splice(index, 1);
      },
      removeMoniteredPaper(index){
        this.deleteMoniteredPaper({token: this.auth.token, pid: this.moniteredPapers[index].id});
        this.moniteredPapers.splice(index, 1);
      },
      removeCollectionPaper(c_index, index){
        const collection_name = this.collections[c_index].name;
        const c_pid = this.collections[c_index].papers[index].id;
        this.deletePaperFromCollection({token: this.auth.token, pid: c_pid, collectionName: collection_name})
        this.collections[c_index].papers.splice(index, 1)
      },
      deleteACollection(c_index){

        this.deleteACollection({token: this.auth.token, collectionName: this.collections[c_index].name});
        this.collections.splice(c_index, 1);
        this.c_delete_dialog = false;
      },
      renameCollection(c_index){
        this.renameCollection({token: this.auth.token, currCollectionName: this.collections[c_index].name, newCollectionName: this.rename_temp});
        this.collections[c_index].name = this.rename_temp;
        this.rename_temp = "";
        this.c_rename_dialog = false;
      }
    },
    mounted() {

      if (!this.auth.loggedIn) {
        this.$router.push("/login");
      }
      else {
        this.getUserProfile({token: this.auth.token})
        .then(async (response) => {
          this.profile = response;
          console.log(this.profile)
          this.likedPapers = await this.getPaperswithPaperIds({pids: this.profile.liked_papers})
          this.moniteredPapers = await this.getPaperswithPaperIds({pids: this.profile.monitered_papers})
          console.log("liked paper length")
          console.log(this.likedPapers)
          console.log(this.likedPapers.length)
          for (const i in this.profile.collections){
            let collection = this.profile.collections[i]
            let collection_paper = []
            if ("paper_id_list" in collection){
              collection_paper = await this.getPaperswithPaperIds({pids: collection.paper_id_list})
            }
            this.collections.push({name: collection.collection_name, papers: collection_paper})
          }
        });
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
