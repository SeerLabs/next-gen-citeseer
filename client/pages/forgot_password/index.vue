<template>
    <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Please enter the email address associated with your account</h2>

          <form method="post" @submit.prevent="sendEmail">
            <div class="field">
              <label class="label">Email address</label>
              <div class="control">
                <v-text-field
                  v-model="email"
                  :rules="['Required']"
                  type="email"
                  class="input"
                  name="password"
                />
              </div>
            </div>
            <div class="control">
              <v-btn type="submit" class="button is-dark is-fullwidth">Change Password</v-btn>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'

export default {
    data() {
      return {
        email: ""
      }
    },
    methods: {
      ...mapMutations(['showNotification']),
      ...mapActions(['sendPasswordResetEmail']),
      sendEmail() {
        this.sendPasswordResetEmail({email: this.email})
        .then(response => {
            if (response.status === 200) {
              this.showNotification({
                text: "Password reset email set. Please check your inbox",
                type: "success"
              })

              this.$router.push('/login')
            }
          }
        ).catch((error) => {
            this.showNotification({
              text: `Error: ${error.message}`,
              type: "error"
            })
        })
        
      }
  },
}
</script>

<style>

</style>