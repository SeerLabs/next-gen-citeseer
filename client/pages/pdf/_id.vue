<template>
  <div>
    <object v-if="!pdfError" id="fit-screen" :data="pdfURL" type="application/pdf" width="100%" height="1000px">
      <embed :src="pdfURL" type="application/pdf" width="100%" height="1000px"/>
    </object>
    <div v-else>{{ pdfError }}</div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      pdfURL: `https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=`,
      pdfError: null
    }
  },
  mounted () {
    try {
      this.pdfURL += this.$route.params.id
    } catch(err) {
      this.pdfError = 'pdf not found error'
    }
  }
}
</script>



