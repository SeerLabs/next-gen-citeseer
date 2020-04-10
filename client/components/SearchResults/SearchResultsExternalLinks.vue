<template>
  <b-container id="search-result-external-links">
    <BaseCardHeader>Try your query at</BaseCardHeader>
    <b-row>
      External Links
    </b-row>
  </b-container>
</template>

<script>
    import BaseCardHeader from "../Base/BaseCardHeader.vue";

    const card_header = new Vue({
      template: ''
    })
    export default {
        name: "SearchResultsExternalLinks",
        components: {
          BaseCardHeader
      }
    }
</script>

<style scoped>
</style>
