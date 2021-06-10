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
                        v-model="collection_dialog"
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
                                    v-model="selected_collection"
                                    :items="collection_names"
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
                                    v-model="new_collection_name"
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
                                @click="collection_dialog = false"
                            >
                                Close
                            </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog
                        v-model="correct_error_dialog"
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
                                Our staffs will manually review the rquest for correcting paper's metadata.
                            <v-container>
                                <v-row>
                                <v-col cols="12">
                                    Title*
                                    <v-text-field
                                    v-model="temp_title"
                                    required
                                    ></v-text-field>
                                </v-col>
                                
                                <v-col cols="12">
                                    Abstract
                                    <v-textarea v-model="temp_abstract">
                                    </v-textarea>
                                </v-col>
                                
                                <v-col cols="12">
                                    Authors
                                    <div v-for="(author_name, index) in temp_authors" :key="index" class="form-row">
                                            
                                            <v-text-field v-model="temp_authors[index]"></v-text-field>
                                            <button type="button" class="close" aria-label="Close" @click="temp_authors.splice(index,1)">
                                                <span aria-hidden="true">×</span>
                                            </button>
                                    </div>
                                    <v-btn
                                        color="blue darken-1"
                                        text
                                        @click="temp_authors.push('')"
                                    >
                                        Add Author
                                    </v-btn>
                                </v-col>
                                
                                <v-col cols="12">
                                    Venue or Conference
                                    <v-text-field v-model="temp_meeting"
                                    ></v-text-field>
                                </v-col>
                                
                                <v-col cols="12" >
                                    Year
                                    <v-text-field v-model="temp_pub_date"
                                    ></v-text-field>
                                </v-col>
                                
                                <v-col cols="12" >
                                    Publisher
                                    <v-text-field v-model="temp_publisher"
                                    ></v-text-field>
                                </v-col>
                                 <v-col cols="12">
                                    Reason Or Details*
                                    <v-text-field
                                    v-model="temp_reason"
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
                                @click="correct_error_dialog = false"
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
                        <v-btn v-if="admin_loggedIn">
                            {{ "Physical Delete Paper" }}
                        </v-btn>
                        <v-btn v-if="admin_loggedIn" >
                            {{ "Logical Delete Paper" }}
                        </v-btn>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
import { mapState } from 'vuex'
import authService from '~/api/AuthService'

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
            collection_dialog: false,
            collection_names: [],
            new_collection_name: '',
            selected_collection: null,
            correct_error_dialog: false,
            loading: true,
            temp_title: this.title,
            temp_authors: this.authors,
            temp_meeting: this.venue,
            temp_pub_date: this.year,
            temp_abstract: this.abstract,
            temp_reason: '',
            temp_publisher: '',
            admin_loggedIn:  false,
        };
    },
    computed: {
        ...mapState(['auth']),
        
        ...mapState(['admin_auth']),

        getPDFUrl() {
            return '/pdf/' + this.docId;
        }
    },
    beforeMount() {
        this.admin_loggedIn = this.admin_auth.loggedIn
      if (this.auth.loggedIn) {
        authService.getUserProfile(this.auth.token)
        .then((response) => {
          const profile = response.data;
          this.liked = profile.liked_papers.includes(this.docId)
          this.monitered = profile.monitered_papers.includes(this.$docId)
          for (const i in profile.collections){
            this.collection_names.push(profile.collections[i].collection_name)
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
        toggleReadMore() {
            this.showAbstract = !this.showAbstract;
        },

        toggleLikePaper() {
          if (!this.liked) {
            authService.addLikedPaper(this.auth.token, this.docId)
          }
          else {
            authService.deleteLikedPaper(this.auth.token, this.docId)
          }
          this.liked = !this.liked
        },

        toggleMoniterPaper() {
          if (!this.monitered) {
            authService.addMoniteredPaper(this.auth.token, this.docId)
          }
          else {
            authService.deleteMoniteredPaper(this.auth.token, this.docId)
          }
          this.monitered = !this.monitered
        },

        addExistingCollectionPaper() {
            if (this.selected_collection){
                authService.addPaperToCollection(this.auth.token, this.docId, this.selected_collection)
                this.collection_dialog = false
            }
            else{
                alert("Please select an existing collection")
            }
            
        },
        
        addToNewCollection(){
            if (this.new_collection_name){
                authService.addCollectionName(this.auth.token, this.new_collection_name)
                authService.addPaperToCollection(this.auth.token, this.docId, this.new_collection_name)
                this.collection_dialog = false;
            }
            else{
                alert("Please enter name of new collection.")
            }
        },

        submitCorrectMetadataRequest(){
            const correctAuthors = []
            if (!this.temp_pub_date){
                this.temp_pub_date = ""
            }
            for (const i in this.temp_authors){
                correctAuthors.push({
                    "name": this.temp_authors[i],
                    "affiliation": "",
                    "address": "",
                    "email": ""
                })
            }
            authService.edit_new(this.auth.token, this.docId, this.temp_reason, this.temp_title, this.temp_abstract, correctAuthors,  this.temp_meeting, this.temp_publisher, this.temp_pub_date.toString())
            this.correct_error_dialog = false;
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
