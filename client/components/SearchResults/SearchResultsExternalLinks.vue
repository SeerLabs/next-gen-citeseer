<template>
  <b-container id="search-result-external-links">
    <base-card :title="filter_title">
        <b-row>
          <b-col cols="12">
            LINKS
          </b-col>
        </b-row>

    </base-card>
  </b-container>
</template>

<script>
    import BaseCard from "../Base/BaseCard.vue";

    export default {
        name: "SearchResultsExternalLinks",
        components: {
          BaseCard
      },

      data() {
          return {
            filter_title: "Try your query at",
          }
      }
    }
</script>

<style scoped>

</style>
