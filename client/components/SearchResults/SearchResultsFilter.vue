<template>
  <div id="search-result-external-links">
    <base-card :title="filter_title">
        <b-row>
          <b-col cols="1">
            <label for="year-filter">Year</label>
          </b-col>

          <b-col cols="11" id="year-filter-value">
            1999 - {{ value }}
          </b-col>
        </b-row>

        <b-row>
          <b-col cols="12">
            <b-form-input id="year-filter" v-model="value" type="range" min="1999" max="2020"/>
          </b-col>
        </b-row>

    </base-card>
  </div>
</template>

<script>
    import BaseCard from "../Base/BaseCard.vue";

    export default {
        name: "SearchResultsFilter",
        components: {
          BaseCard
      },

      data() {
          return {
            filter_title: "Filter results",
            value: 2020
          }
      }
    }
</script>

<style scoped>
  #year-filter-value {
    text-align: right;
  }
</style>
