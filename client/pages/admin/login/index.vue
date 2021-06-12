<template>
  <section class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-4 is-offset-4">
          <h2 class="title has-text-centered">Admin Login</h2>

          <Notification v-if="error" :message="error"/>

          <form method="post" @submit.prevent="submitLogin">
            <div class="field">
              <label class="label">Username</label>
              <div class="control">
                <v-text-field
                  v-model="username"
                  type="text"
                  class="input"
                  name="username"
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
          <!-- <div class="has-text-centered" style="margin-top: 20px">
            <p>
              Don't have an account? <nuxt-link to="/register">Register</nuxt-link>
            </p>
            <p>
              Forgot password? <nuxt-link to="/forgot_password">Click here</nuxt-link>
            </p>
          </div> -->
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapMutations, mapState, mapActions } from 'vuex'
import Notification from '~/components/Notification'

export default {
  components: {
    Notification,
  },
  data() {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  computed: {
    ...mapState(['admin_auth'])
  },
  /*
  async beforeCreate() {
    if (this.auth && this.auth.token) {
        this.$router.push("/myciteseer/profile")
    }
    else {
      try {
        // await this.$recaptcha.init()
      } catch(e) {
        // eslint-disable-next-line
        console.log(e);
      }
    }
  }, */
  methods: {
    ...mapMutations('admin_auth', ['admin_login']),
    ...mapMutations(['showNotification']),
    ...mapActions(['loginAdmin']),
    async submitLogin() {
      try {
        // const recaptchaToken = await this.$recaptcha.execute('login');
        // const recaptchaStatus = (await authService.checkRecaptcha(recaptchaToken)).data.success;
        // if (true) {
          await this.loginAdmin(this.username, this.password)
          .then((response) => {
            if (response.status === 200) {
              const user = response.data;
              this.admin_login(user);
              this.$router.push('/admin/console')
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
      } catch(error) {
          // eslint-disable-next-line
          console.log(error);
      }
    },
  },
}
</script>