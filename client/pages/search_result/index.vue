<template>
  <div>
    <navbar/>
    <search-result-list/>
  </div>
</template>

<script>
import Navbar from '~/components/Navbar.vue'
import SearchResultList from "../../components/SearchResults/SearchResultsList.vue";

export default {
  components: {
    SearchResultList,
    Navbar
  }
}
</script>

<style>
</style>
