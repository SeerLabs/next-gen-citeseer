<template>
    <div id="app">
      <h1>Search Engine</h1>
      <search-box/>
    </div>
</template>

<script>
import SearchBox from '~/components/SearchBox.vue'
export default {
  components: {
    SearchBox
  },
  layout: 'layout_default',
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 10% auto;
}
</style>
