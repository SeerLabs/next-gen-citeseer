<template>
  <b-container class="base-card">
    <b-row>
      <b-col cols="12" class="card-header">
        <h4 v-text="title" />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" class="card-body">
        <slot></slot>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
    export default {
        name: "SearchResultsContent",
        props: {
          title: String
        }
    };
</script>

<style scoped>
  .base-card {
    margin-bottom: 1em;
    border: 1px darkgrey solid;
  }
</style>
