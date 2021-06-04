
<template>
  <object id="fit-screen" :data="pdfURL" type="application/pdf">
    <embed :src="pdfURL" type="application/pdf">
  </object>
</template>

<script>

export default {
  data () {
    return {
      pdfURL: `${this.$axios.defaults.baseURL}/document?repid=rep1&type=pdf&doi=`
    }
  },
  mounted () {
    this.pdfURL += this.$route.params.id
  }
}
</script>

<style>
#fit-screen {
   margin: 0px;
   height: 100vh;
   width: 100%;
}
</style>
