<template>
    <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Please enter your new password</h2>

          <form method="post" @submit.prevent="submitPassword">
            <div class="field">
              <label class="label">Password</label>
              <div class="control">
                <v-text-field
                  v-model="password"
                  :rules="['Required']"
                  type="password"
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
import { mapMutations } from 'vuex'
import authService from '~/api/AuthService'

export default {
    data() {
      return {
        password: ""
      }
    },
    methods: {
      ...mapMutations(['showNotification']),

      submitPassword() {
        authService.resetPassword(this.password, this.$route.params.token)
        .then(response => {
            if (response.status === 200) {
              this.showNotification({
                text: "Password changed successfully. You may now login to your account.",
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

            this.$router.push('/login')
        })
        
      }
  },
}
</script>

<style>

</style>