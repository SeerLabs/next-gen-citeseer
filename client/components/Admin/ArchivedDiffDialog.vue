
<template>
    <v-row no-gutters>
        <v-col cols="12" class="result-title">
            <v-dialog
            v-model="dialog"
            fullscreen
            hide-overlay
            :retain-focus="false"
            transition="dialog-bottom-transition"
            >
            <template v-slot:activator="{ on, attrs }">
                <h4 class="font-weight-medium"
                v-bind="attrs"
                v-on="on"
                >
                <div v-if="req.status === 'DENIED'">
                <p style="color:red;">Status: {{req.status}}</p>
                </div>
                <div v-if="req.status === 'COMMITTED'">
                <p style="color:green;">Status: {{req.status}}</p>
                </div>
                <h6>Submitted by:  {{ req.requester_email}}</h6>
                
                {{ paper.title}}
                </h4>
            </template>
            <v-card>
                <v-toolbar
                dark
                color="#2c3e50"
                >
                <v-btn
                    icon
                    dark
                    @click="dialog = false"
                >
                X
                    <!-- <v-icon>mdi-close</v-icon> -->
                </v-btn>
                <v-toolbar-title>Metadata Diff</v-toolbar-title>
                <v-spacer></v-spacer>
                <!-- <v-toolbar-items>
                    <v-btn
                    dark
                    color="error"
                    @click="rejectReq()"
                    >
                    Reject Request
                    </v-btn>
                </v-toolbar-items>
                <v-toolbar-items>
                    <v-btn
                    dark
                    color="success"
                    @click="commitReq()"
                    >
                    Commit Changes
                    </v-btn>
                </v-toolbar-items> -->
                </v-toolbar>
                <v-list
                three-line
                subheader
                >
            <v-row >
            <v-col md="6" class="scroll">
                
                 <v-col>
                        Reviewer Comment
                        <v-text-field v-model="reviewer_comment"
                        ></v-text-field>
                </v-col>
                <v-col v-if="req.title != '' && req.title != paper.title" class="request-field">
                        Requested Title
                        <v-text-field v-model="req.title"
                        ></v-text-field>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Title
                        <v-text-field
                        v-model="paper.title"
                        ></v-text-field>
                        
                    </v-col>
                    <!-- <v-col v-if="req.title != '' && req.title != paper.title">
                        <v-btn-toggle
                        v-model="toggle[0]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col> -->
                </v-col>

                
                <v-col v-if="req.abstract != '' && req.abstract != paper.abstract" class="request-field">
                        Requested Abstract
                        <v-textarea v-model="req.abstract"
                        ></v-textarea>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Abstract
                        <v-textarea v-model="paper.abstract">
                        </v-textarea>
                    </v-col>
                    <!-- <v-col v-if="req.abstract != '' && req.abstract != paper.abstract">
                        <v-btn-toggle
                        v-model="toggle[1]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col> -->
                </v-col>


                <v-col class="field_bottom_pad">
                    <v-col>
                        
                        Authors
                        <div v-for="(author, index) in paper.authors" :key="index" class="form-row">
                                
                                <v-text-field v-model="paper.authors[index]"></v-text-field>
                                <button type="button" class="close" aria-label="Close" @click="paper.authors.splice(index,1)">
                                    <span aria-hidden="true">×</span>
                                </button>
                        </div>
                        <v-btn
                            color="blue darken-1"
                            text
                            @click="paper.authors.push('')"
                        >
                            Add Author
                        </v-btn>
                    </v-col>
                </v-col>

                
                <v-col v-if="req.meeting != '' && req.meeting != paper.meeting" class="request-field">
                        Requested Venue Or Conference
                        <v-text-field v-model="req.meeting"
                        ></v-text-field>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Venue Or Conference
                        <v-text-field v-model="paper.venue"
                        ></v-text-field>
                    </v-col>
                    <!-- <v-col v-if="req.meeting != '' && req.meeting != paper.venue">
                        <v-btn-toggle
                        v-model="toggle[3]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col> -->
                </v-col>


                <!-- <v-col v-if="req.venue_type != '' && req.venue_type != paper.venue_type" class="request-field">
                        Requested Venue Type
                        <v-text-field v-model="req.venue_type"
                        ></v-text-field>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Venue Type
                        <v-text-field v-model="paper.venue_type"
                        ></v-text-field>
                    </v-col>
                    <v-col v-if="req.venue_type != '' && req.venue_type != paper.venue_type">
                        <v-btn-toggle
                        v-model="toggle[4]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col>
                </v-col> -->

                <v-col v-if="req.pub_date != '' && req.pub_date != paper.pub_date" class="request-field">
                        Requested year
                        <v-text-field v-model="req.pub_date"
                        ></v-text-field>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Year
                        <v-text-field v-model="paper.year"
                        ></v-text-field>
                    </v-col>
                    <!-- <v-col v-if="req.pub_date != '' && req.pub_date != paper.year">
                        <v-btn-toggle
                        v-model="toggle[4]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col> -->
                </v-col>
                
                <v-col v-if="req.publisher != '' && req.publisher!= paper.publisher" class="request-field">
                        Requested Publisher
                        <v-text-field v-model="req.publisher"
                        ></v-text-field>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Publisher
                        <v-text-field v-model="paper.publisher"
                        ></v-text-field>
                    </v-col>
                    <!-- <v-col v-if="req.publisher != '' && req.publisher != paper.publisher">
                        <v-btn-toggle
                        v-model="toggle[5]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col> -->
                </v-col>
               
                

                <!-- <v-col v-if="req.pub_address != '' && req.pub_address != paper.pub_address" class="request-field">
                        Requested Publisher Address
                        <v-text-field v-model="req.pub_address"
                        ></v-text-field>
                </v-col>
                <v-col class="field_bottom_pad">
                    <v-col>
                        Publisher Address
                        <v-text-field v-model="paper.pub_address"
                        ></v-text-field>
                    </v-col>
                    <v-col v-if="req.pub_address != '' && req.pub_address != paper.pub_address">
                        <v-btn-toggle
                        v-model="toggle[7]"
                        mandatory
                        color="success"
                        >
                        <v-btn text>
                            Not Selected
                        </v-btn>
                        <v-btn text>
                            Use Current
                        </v-btn>
                        <v-btn text>
                            Use Requested
                        </v-btn>
                        
                        </v-btn-toggle>
                    </v-col>
                </v-col> -->

                
            </v-col>
            <v-col md="6">
                <object id="fit-screen"  :data="pdfURL" type="application/pdf">
                    <embed :src="pdfURL" type="application/pdf">
                </object>
            </v-col>
            </v-row>


                
                </v-list>
            </v-card>
            </v-dialog>
                
        </v-col>
        
        
    </v-row>
</template>

<script>
import { mapState } from 'vuex'
import authService from '~/api/AuthService'
  export default {
    props: {
        paper: null,
        metaRequest: null,
    },
    data () {
      return {
        pdfURL: 'http://localhost:8115/api/document?repid=rep1&type=pdf&doi=',
        dialog: false,
        notifications: false,
        sound: true,
        widgets: false,
        req: this.metaRequest.user_request,
        req_id: this.metaRequest.request_id,
        reviewer_comment: this.metaRequest.user_request.reviewer_comment,
        
        toggle: [],
      }
    },
     computed: {
      ...mapState(['admin_auth'])
    },
    mounted(){
        this.pdfURL += this.paper.id
        let i;
        for (i = 0; i < 6; i++) {
            this.toggle.push(undefined)
        }
    },
    methods: {
        commitReq(){
            let i;
            for (i = 0; i < 6; i++) {
                if (typeof this.toggle[i] !=='undefined' && this.toggle[i] === 0){
                    alert("There are unreviewed fields, please select them all.")
                    return
                }
            }
            authService.edit_commit(this.admin_auth.token, this.req_id, this.reviewer_comment)
            this.dialog = false;
        },
        rejectReq(){
            let i;
            for (i = 0; i < 6; i++) {
                if (typeof this.toggle[i] !=='undefined' && this.toggle[i] === 0){
                    alert("There are unreviewed fields, please select them all.")
                    return
                }
            }
            
            authService.edit_deny(this.admin_auth.token, this.req_id, this.reviewer_comment)
            this.dialog = false;
        }
    }
  }
</script>
<style>
.request-field {
    background-color: rgb(255, 239, 239);
}
#fit-screen {
   margin: 0px;
   height: 90vh;
   width: 100%;
}
.field_bottom_pad {
    padding-bottom: 10%;
}
.scroll {
  width: 100%;
  height: 90vh;
  overflow: scroll;
}
</style>