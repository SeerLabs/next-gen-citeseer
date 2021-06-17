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
                            v-model="fullName"></v-text-field>
                        </v-col>
                      </v-row>
                      
                      <v-row>
                        <v-col cols="2">
                          Email
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="email"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Organization
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="organization"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Department
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="department"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Web Page
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="webPage"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          State
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="state"></v-text-field>
                        </v-col>
                      </v-row>

                      <v-row>
                        <v-col cols="2">
                          Country
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                            v-model="country"></v-text-field>
                        </v-col>
                      </v-row>

                      
                      
                      <v-card-actions>
                        <v-btn :loading="loading" @click.native="profileUpdate">
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
    data() {
      return {
        fullName: this.profile.full_name,
        email: this.profile.email,
        organization:this.profile.organization,
        department: this.profile.department,
        webPage: this.profile.web_page,
        state: this.profile.state,
        country: this.profile.country,
      }
    },
    methods: {
      ...mapActions(['sendPasswordResetEmail', 'updateProfile']),
      sendResetPasswordEmail(){
        this.sendPasswordResetEmail({email: this.email})
      },
      profileUpdate(){
          this.updateProfile({email: this.email})
      }
      
    },
    
};
</script>

<style scoped>

</style>