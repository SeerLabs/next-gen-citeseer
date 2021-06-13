<template>
    <div>
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
                        <v-btn :loading="loading" @click.native="updateProfile">
                            <v-icon left dark>check</v-icon>
                            Update Profile Information
                        </v-btn>
                      </v-card-actions>
                      
                      
                    </v-card-text>
                    
                  </v-card>
                </v-layout>
    </div>
</template>
<script>
import { mapActions } from 'vuex'

export default {

    props: {
        profile: { type: Object, default: null},
    },
    methods: {
      ...mapActions(['sendPasswordResetEmail', 'updateProfile']),
      sendResetPasswordEmail(){
        this.sendPasswordResetEmail({email: this.profile.email})
      },
      updatePrifle(){
          this.updateProfile({email: this.profile.email})
      }
      
    },
    
};
</script>

<style scoped>

</style>