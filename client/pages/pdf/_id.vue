
<template>
  <object id="fit-screen" :data="pdfURL" type="application/pdf">
    <embed :src="pdfURL" type="application/pdf" width="100%" height="1000px"/>
  </object>
</template>

<script>

export default {
  data () {
    return {
      pdfURL: `https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=`
    }
  },
  mounted () {
    this.pdfURL += this.$route.params.id
  }
}
</script>


