<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Register!</h2>

          <Notification v-if="error" :message="error"/>

          <form method="post" @submit.prevent="register">
            <div class="field">
              <label class="label">Email</label>
              <div class="control">
                <v-text-field
                  v-model="email"
                  type="email"
                  class="input"
                  name="email"
                  required
                />
              </div>
            </div>
            <div class="field">
              <label class="label">Full Name</label>
              <div class="control">
                <v-text-field
                  v-model="fullName"
                  type="text"
                  class="input"
                  name="fullName"
                  required
                />
              </div>
            </div>
            <div class="field">
              <label class="label">Password</label>
              <div class="control">
                <v-text-field
                  v-model="password"
                  type="password"
                  class="input"
                  name="password"
                  required
                />
              </div>
            </div>
            <div class="control">
              <v-btn type="submit">Register</v-btn>
            </div>
          </form>

          <div class="has-text-centered" style="margin-top: 20px">
            Already got an account? <nuxt-link to="/login">Login</nuxt-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapGetters, mapMutations, mapActions } from 'vuex'
import Notification from '~/components/Notification'

export default {
  components: {
    Notification,
  },
  data() {
    return {
      email: '',
      fullName: '',
      password: '',
      error: null
    }
  },
  computed: {
    ...mapGetters({
        loggedIn: 'auth/loggedIn',
  })},
  created() {
      if (this.loggedIn) {
        this.$router.push("/myciteseer/profile")
      }
  },

  methods: {
    ...mapMutations(['showNotification']),
    ...mapActions(['checkRecaptcha', 'registerUser']),
    async register() {
      try {
        const token = await this.$recaptcha.execute('login');
        const recaptchaStatus = (await this.checkRecaptcha(token)).data.success;

        if (recaptchaStatus) {
          await this.registerUser({email: this.email, password: this.password, fullName: this.fullName})
          .then((response) => {
            if(response.status === 200) {
              this.$router.push('/login');
              this.showNotification({ 
                  text: "Account successfully created. Please check your inbox for a confirmation email to login.", 
                  type: "success"
                })
            }
            else {
              this.showNotification({
                  text: "Error creating account. Please try again.",
                  type: "error"
                })
            }
          });
        }
      } catch(error) {
        // eslint-disable-next-line
        console.log(error);
      }
    }
  }
}
</script>