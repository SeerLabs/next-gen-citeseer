<template>
  <div></div>
</template>

<script>
import { mapMutations } from 'vuex'
import authService from '~/api/AuthService'

export default {
  created() {
    authService.activateUser(this.$route.params.token)
    .then(response => {
      const success = response.data.success
      if (success) {
        this.showNotification({
          text: "Account activated successful. You may now login to your account.",
          type: "success"
        })
      }
      else {
        this.showNotification({
          text: "Error: Invalid token.",
          type: "error"
        })
      }

      this.$router.push('/login')
    })

    this.$router.push('/login')
    },
    methods: {
      ...mapMutations(['showNotification'])
    }
}
</script>

<style>

</style>