<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Welcome back!</h2>

          <Notification v-if="error" :message="error"/>

          <form method="post" @submit.prevent="submitLogin">
            <div class="field">
              <label class="label">Email</label>
              <div class="control">
                <v-text-field
                  v-model="email"
                  type="text"
                  class="input"
                  name="email"
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
                />
              </div>
            </div>
            <div class="control">
              <v-btn type="submit" class="button is-dark is-fullwidth">Log In</v-btn>
            </div>
          </form>
          <div class="has-text-centered" style="margin-top: 20px">
            <p>
              Don't have an account? <nuxt-link to="/register">Register</nuxt-link>
            </p>
            <p>
              Forgot password? <nuxt-link to="/forgot_password">Click here</nuxt-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapMutations, mapState } from 'vuex'
import Notification from '~/components/Notification'
import authService from '~/api/AuthService'

export default {
  components: {
    Notification,
  },
  data() {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  computed: {
    ...mapState(['auth'])
  },
  async beforeCreate() {
    if (this.auth && this.auth.token) {
        this.$router.push("/myciteseer/profile")
    }
    else {
      try {
        await this.$recaptcha.init()
      } catch(e) {
        // eslint-disable-next-line
        console.log(e);
      }
    }
  },
  methods: {
    ...mapMutations('auth', ['login']),
    ...mapMutations(['showNotification']),
    async submitLogin() {
      try {
        const recaptchaToken = await this.$recaptcha.execute('login');
        const recaptchaStatus = (await authService.checkRecaptcha(recaptchaToken)).data.success;

        if (recaptchaStatus) {
          await authService.loginUser(this.email, this.password)
          .then((response) => {
            if (response.status === 200) {
              const user = response.data;
              this.login(user);
              this.$router.push('/')
            }
            else if (response.status === 401) {
              this.showNotification({
                text: "Login unsuccessful, invalid email address or password.",
                type: "error"
              })
            }
          })
          .catch((error) => {
              this.showNotification({
                text: `Error: ${error.message}`, 
                type: "error"
              })

              // eslint-disable-next-line
              console.log(error);

          });
        }
      } catch(error) {
          // eslint-disable-next-line
          console.log(error);
      }
    },
  },
}
</script>