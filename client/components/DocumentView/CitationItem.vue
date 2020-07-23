<template>
  <b-container fluid="sm" class="document-result">
    <b-row>
      <b-col class="result-title"><h4><nuxt-link :to="'/show_citing/' + cid">{{ title }}</nuxt-link></h4></b-col>
      <!-- <b-col cols="6" class="result-type">{{ type }}</b-col> -->
    </b-row>

    <b-row>
      <b-col class="result-info"><h6>{{ authors }} - {{ venue }} - {{ year }}</h6></b-col>
    </b-row>
     
    <!-- <b-row>
      <b-col class="result-content">
        <p>
            <span v-if="!readMoreToggle">{{abstract.slice(0, 200)}}</span>
            <a class="" v-if="!readMoreToggle" @click="toggleReadMore" href="#">
                Read more...
            </a>
            <span v-if="readMoreToggle" v-html="abstract"></span>
        </p>
      </b-col>
    </b-row> -->

    <!-- <b-row>
      <b-col cols="3" class="citations">
        Cited by {{ numCitations }}
      </b-col>
      <b-col cols="9" class="links">
        <a href="http://google.com">+Cite</a>
        <a href="http://google.com">+View PDF</a>
        <a href="http://google.com">+Save</a>
        <a href="http://google.com">+Add to ExportCart</a>
      </b-col>
    </b-row> -->

  </b-container>
</template>

<script>
    export default {
        name: "DocumentResultsItem",
        props: {
          title: String,
          type: String,
          authors: String,
          venue: String,
          year: String,
          abstract: String,
          numCitations: Number,
          cid: Number,
        },
        data(){
          return {
            readMoreToggle: false,
            url: ""
          }
        },
        methods: {
            toggleReadMore(){
                this.readMoreFlag = true
            }
        },
        created() {
          if (!this.$props.title) { this.$props.title = "Title Not Indexed" }
          if (!this.$props.authors) { this.$props.authors = "Authors Not Indexed"}
          if (!this.$props.venue) { this.$props.venue = "Venue Not Indexed"}
          if (!this.$props.year) { this.$props.year = "Year Not Indexed"}
        }
       
    }
</script>

<style scoped>
  .document-result {
    background-color: white;
    padding: 1rem;
    border-bottom:1px solid gray;
  }
  .result-type {
    text-align: right;
    font-weight: 600;
  }

  .result-info {
    margin-bottom: .5em;
  }

  .result-content {
    margin-bottom: .3em;
  }

  .links {
    text-align: right;
  }

  .links a {
    margin-left: 1em;
  }
</style>
