<template>
  <div>
    <div id = app>
      <h1>Search Engine</h1>
      <search-box/>
    </div>
  </div>
</template>

<script>
//import Navbar from '~/components/Navbar.vue'
import SearchBox from '~/components/SearchBox.vue'
//import default from '~/layouts/default.vue'
export default {
  components: {
   // Navbar,
    //default,
    SearchBox

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10%;
  margin-left: 25%;
  margin-right: 25%;
  margin-bottom: 10%;
}
</style>
