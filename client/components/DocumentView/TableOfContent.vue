<template>
  <b-card>
    <b-row>
      <b-col><h6 v-on:click="scroll" >Citation</h6></b-col>
    </b-row>
   <b-row>
      <b-col><h6>Similar Article</h6></b-col>
    </b-row>
   <b-row>
      <b-col><h6>Version History</h6></b-col>
    </b-row>
    
  </b-card>
</template>

<script>
    export default {
        name: "Table of Content",
        methods: {
            scroll () {
              document.getElementById(index).scrollIntoView();
            }
        }
    };
</script>
<style>
</style>