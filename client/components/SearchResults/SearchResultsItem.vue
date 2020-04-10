<template>
  <b-container fluid="sm" class="search-result">
    <b-row>
      <b-col cols="6" class="result-title"><h4>Document Title</h4></b-col>
      <b-col cols="6" class="result-type">DOCUMENT</b-col>
    </b-row>

    <b-row>
      <b-col class="result-info"><h6>FirstName, LastName - 2018</h6></b-col>
    </b-row>

    <b-row>
      <b-col class="result-content">
        <p>
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        </p>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="3" class="citations">
        Cited by
      </b-col>
      <b-col cols="9" class="links">
        <a href="http://google.com">+Cite</a>
        <a href="http://google.com">+View PDF</a>
        <a href="http://google.com">+Save</a>
        <a href="http://google.com">+Add to ExportCart</a>
      </b-col>
    </b-row>

  </b-container>
</template>

<script>
    export default {
        name: "SearchResultsItem"
    }
</script>

<style scoped>
  .search-result {
    background-color: red;
    padding: 1.5rem;
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
