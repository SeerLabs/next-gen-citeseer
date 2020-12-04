<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Register!</h2>

          <Notification v-if="error" :message="error"/>

          <form method="post" @submit.prevent="register">
            <div class="field">
              <label class="label">Username</label>
              <div class="control">
                <v-text-field
                  v-model="username"
                  type="text"
                  class="input"
                  name="username"
                  required
                />
              </div>
            </div>
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
                  v-model="full_name"
                  type="text"
                  class="input"
                  name="full_name"
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
import { mapGetters } from 'vuex'
import Notification from '~/components/Notification'
import authService from '~/api/AuthService'

export default {
  components: {
    Notification,
  },
  data() {
    return {
      username: '',
      email: '',
      full_name: '',
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
    async register() {
      try {
        const token = await this.$recaptcha.execute('login');
        const recaptchaStatus = (await authService.checkRecaptcha(token)).data.success;

        if (recaptchaStatus) {
          await authService.registerUser(this.username, this.password, this.email, this.full_name)
          .then((response) => {
            if(response.status === 200) {
              this.$router.push('/login');
            }
          });
        }
      } catch(error) {
        // eslint-disable-next-line
        console.log(error);
      }
    }
  },
  layout: 'layout_default'
}
</script>