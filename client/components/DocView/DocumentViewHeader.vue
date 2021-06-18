<template>
    <v-row id="doc-view-header">
        <v-col cols="9">
            <h2>{{ title }}</h2>
            <h5>{{ authors.join(', ') }}</h5>
            <h5>{{ venue }} - {{ year }}</h5>
            <br />

            <div
                id="abstract"
                :style="
                    showAbstract
                        ? { height: 'min-content' }
                        : { maxHeight: '150px' }
                "
            >
                <p>{{ abstract }}</p>
            </div>
            <v-btn @click="() => (showAbstract = !showAbstract)">
                {{ !showAbstract ? 'Show more' : 'Show less' }}
            </v-btn>
        </v-col>
        <v-col cols="3">
            <v-card id="document-options">
                <v-card-text class="d-flex flex-column mb-6">
                    <!-- PDF Button -->
                    <v-btn
                        id="pdf-btn"
                        squared
                        :href="getPDFUrl"
                        target="_blank"
                        class="mv-md-2"
                    >
                        View PDF
                    </v-btn>

                    <v-btn @click="toggleMoniterPaper">
                      {{ monitered ? "Unmoniter Paper" : "Moniter Paper" }}
                    </v-btn>

                    <v-btn @click="toggleLikePaper">
                      {{ liked ? "Unlike Paper" : "Like Paper" }}
                    </v-btn>

                    <v-dialog
                        v-model="collectionDialog"
                        width="500"
                        >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                            v-bind="attrs"
                            v-on="on"
                            >
                            Add To A Collection
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-title >
                                Existing Collection
                            </v-card-title>
                            <v-card-text>
                                <v-select
                                    v-model="selectedCollection"
                                    :items="collectionNames"
                                    label="Select from a existing collection"
                                    item-value="text"
                                    >
                                    </v-select>
                                <v-btn
                                    @click="addExistingCollectionPaper()"
                                >
                                    Add to Collection
                                </v-btn>
                            </v-card-text>
                            <v-card-title >
                                Make A New Collection
                            </v-card-title>

                            <v-card-text>
                                <v-text-field
                                    v-model="newCollectionName"
                                    label="Collection Name"
                                ></v-text-field>
                                <v-btn
                                    @click="addToNewCollection()"
                                >
                                    Add to New Collection
                                </v-btn>
                            </v-card-text>
                            
                            <v-divider></v-divider>

                            <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                color="primary"
                                text
                                @click="collectionDialog = false"
                            >
                                Close
                            </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog
                        v-model="correctErrorDialog"
                        persistent
                        max-width="600px"
                        >
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn
                            v-bind="attrs"
                            v-on="on"
                            >
                            Correct Error
                            </v-btn>
                        </template>
                        <v-card>
                            <v-card-title>
                            <span class="headline">Request to Correct Errors</span>
                            </v-card-title>
                            <v-card-text>
                                Our staff will manually review the rquest for correcting paper's metadata.
                            <v-container>
                                <v-row>
                                <v-col cols="12">
                                    Title*
                                    <v-text-field
                                    v-model="tempTitle"
                                    required
                                    ></v-text-field>
                                </v-col>
                                
                                <v-col cols="12">
                                    Abstract
                                    <v-textarea v-model="tempAbstract">
                                    </v-textarea>
                                </v-col>
                                
                                <v-col cols="12">
                                    Authors
                                    <div v-for="(author_name, index) in tempAuthors" :key="index" class="form-row">
                                            
                                            <v-text-field v-model="tempAuthors[index]"></v-text-field>
                                            <button type="button" class="close" aria-label="Close" @click="tempAuthors.splice(index,1)">
                                                <span aria-hidden="true">×</span>
                                            </button>
                                    </div>
                                    <v-btn
                                        color="blue darken-1"
                                        text
                                        @click="tempAuthors.push('')"
                                    >
                                        Add Author
                                    </v-btn>
                                </v-col>
                                
                                <v-col cols="12">
                                    Venue or Conference
                                    <v-text-field v-model="tempMeeting"
                                    ></v-text-field>
                                </v-col>
                                
                                <v-col cols="12" >
                                    Year
                                    <v-text-field v-model="tempPubDate"
                                    ></v-text-field>
                                </v-col>
                                
                                <v-col cols="12" >
                                    Publisher
                                    <v-text-field v-model="tempPublisher"
                                    ></v-text-field>
                                </v-col>
                                 <v-col cols="12">
                                    Reason Or Details*
                                    <v-text-field
                                    v-model="tempReason"
                                    required
                                    ></v-text-field>
                                </v-col>
                                
                            
                                
                                </v-row>
                            </v-container>
                            <small>*indicates required field</small>
                            </v-card-text>
                            <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                                color="blue darken-1"
                                text
                                @click="correctErrorDialog = false"
                            >
                                Close
                            </v-btn>
                            <v-btn
                                color="blue darken-1"
                                text
                                @click="submitCorrectMetadataRequest"
                            >
                                Submit
                            </v-btn>
                            </v-card-actions>
                        </v-card>
                        </v-dialog>
                        
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
    props: {
        docId: { type: String, default: '' },
        title: { type: String, default: '' },
        authors: { type: Array, default: null },
        venue: { type: String, default: '' },
        year: { type: String, default: '' },
        nCitation: { type: Number, default: 0 },
        abstract: { type: String, default: '' }
    },
    data() {
        return {
            showAbstract: false,
            liked: false,
            monitered: false,
            collectionDialog: false,
            collectionNames: [],
            newCollectionName: '',
            selectedCollection: null,
            correctErrorDialog: false,
            loading: true,
            tempTitle: this.title,
            tempAuthors: this.authors,
            tempMeeting: this.venue,
            tempPubDate: this.year,
            tempAbstract: this.abstract,
            tempReason: '',
            tempPublisher: '',
        };
    },
    computed: {
        ...mapState(['auth']),
        
        getPDFUrl() {
            return '/pdf/' + this.docId;
        }
    },
    beforeMount() {
      if (this.auth.loggedIn) {
        this.getUserProfile({token: this.auth.token})
        .then((response) => {
          const profile = response.data;
          this.liked = profile.liked_papers.includes(this.docId)
          this.monitered = profile.monitered_papers.includes(this.$docId)
          for (const i in profile.collections){
            this.collectionNames.push(profile.collections[i].collectionName)
          }
          this.loading = false;
        })
      }
      else {
        this.liked = false;
        this.monitered = false;

        this.loading = false;
      }
    },
    methods: {
        ...mapActions(['getUserProfile', 'addLikedPaper', 'deleteLikedPaper', 'addMoniteredPaper', 
        'deleteMoniteredPaper', 'addPaperToCollection', 'addCollectionName', 'addPaperToCollection', 'editNew']),
        toggleReadMore() {
            this.showAbstract = !this.showAbstract;
        },
        isLoggedIn(){
            if (!this.auth.loggedIn) {
                this.$router.push("/login");
                return false;
            }
            return true;
        },
        toggleLikePaper() {
            if (!this.isLoggedIn()) {
                return;
            }
            if (!this.liked) {
                this.addLikedPaper({token: this.auth.token, pid: this.docId})
            }
            else {
                this.deleteLikedPaper({token: this.auth.token, pid: this.docId})
            }
            this.liked = !this.liked
        },

        toggleMoniterPaper() {
            if (!this.isLoggedIn()) {
                return;
            }
            if (!this.monitered) {
                this.addMoniteredPaper({token: this.auth.token, pid: this.docId})
            }
            else {
                this.deleteMoniteredPaper({token: this.auth.token, pid: this.docId})
            }
            this.monitered = !this.monitered
        },

        addExistingCollectionPaper() {
            if (!this.isLoggedIn()) {
                return;
            }
            if (this.selectedCollection){
                this.addPaperToCollection({token: this.auth.token, pid: this.docId, collectionName: this.selectedCollection})
                this.collectionDialog = false
            }
            else{
                alert("Please select an existing collection")
            }
            
        },
        
        addToNewCollection(){
            if (!this.isLoggedIn()) {
                return;
            }
            if (this.newCollectionName){
                this.addCollectionName({token: this.auth.token, collectionName: this.newCollectionName})
                this.addPaperToCollection({token: this.auth.token, pid: this.docId, collectionName: this.newCollectionName})
                this.collectionDialog = false;
            }
            else{
                alert("Please enter name of new collection.")
            }
        },

        submitCorrectMetadataRequest(){
            if (!this.isLoggedIn()) {
                return;
            }
            const correctAuthors = []
            if (!this.tempPubDate){
                this.tempPubDate = ""
            }
            for (const i in this.tempAuthors){
                correctAuthors.push({
                    "name": this.tempAuthors[i],
                    "affiliation": "",
                    "address": "",
                    "email": ""
                })
            }
            this.editNew({
                token: this.auth.token, 
                paperId: this.docId, 
                reasonOrDetails: this.tempReason, 
                title: this.tempTitle, 
                abstract: this.tempAbstract, 
                authors: correctAuthors,  
                meeting: this.tempMeeting, 
                publisher: this.tempPublisher, 
                publishDate: this.tempPubDate.toString()
            })
            this.correctErrorDialog = false;
        }
    }
};
</script>

<style>
#doc-view-layout {
    background: rgb(255, 255, 255);
}

#doc-view-header {
    margin-bottom: 3em;
    background: #ffffff;
}

#abstract {
    overflow: hidden;
}

#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
}

.citation-card {
    margin-bottom: 1em;
}

#pdf-btn {
    background: rgb(235, 0, 0);
    color: white;
    margin-bottom: 1em;
    outline: transparent;
    border-color: transparent;
}
</style>
