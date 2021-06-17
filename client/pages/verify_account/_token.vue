<template>
  <div></div>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'

export default {
  created() {
    this.activateUser({token: this.$route.params.token})
    .then((response) => {
      const success = response.success
      if (success) {
        this.showNotification({
          text: "Account activated successful. You may now login to your account.",
          type: "success"
        })
      }
      else {
        this.showNotification({
          text: "Error: Invalid token. Account activation not successful",
          type: "error"
        })
      }

      this.$router.push('/login')
    })
    .catch((error) => {
      this.showNotification({
        text: "Error: Invalid token. Account activation not successful",
        type: "error"
      })
      
      this.$router.push('/login')
      // eslint-disable-next-line
      console.log(error)
    });
    
    },
    methods: {
      ...mapMutations(['showNotification']),
      ...mapActions(['activateUser'])
    }
}
</script>

<style>

</style>