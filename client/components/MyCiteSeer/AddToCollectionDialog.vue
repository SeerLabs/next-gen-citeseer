<template>
    <v-dialog
        v-model="collectionDialog"
        width="500"
        >
        <template v-slot:activator="{ on, attrs }">
            <v-btn v-if="buttonType == 'viewPage'"
            v-bind="attrs"
            v-on="on"
            >
            Add To A Collection
            </v-btn>
            <a v-if="buttonType == 'searchItem'"
            v-bind="attrs"
            v-on="on"
            >+Save</a>
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
</template>
<script>

import { mapState, mapActions } from 'vuex'
export default{
    props: {
        docId: {type: String},
        collectionNames: {type: Array, default: null},
        buttonType: {type: String, default: "viewPage"}
    },
    data(){
        return {
            collectionDialog: false,
            selectedCollection: null,
            newCollectionName: '',
        };
    },
    computed: {
        ...mapState(['auth']),
    },
    beforeMount() {
        console.log(this.buttonType)
    },
    methods: {
        ...mapActions(['addPaperToCollection','addCollectionName']),
        isLoggedIn(){
            if (!this.auth.loggedIn) {
                this.$router.push("/login");
                return false;
            }
            return true;
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
    }
    

};
</script>
