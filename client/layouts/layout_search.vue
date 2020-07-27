<template>
  <div>
    <nav-bar />
    <b-container fluid="md">
      <b-col id="page-container" cols="12">
        <b-row>
          <b-col id="search-box-container" sm="8">
            <search-box v-model="searchQuery" />
          </b-col>
        </b-row>
        <nuxt keep-alive />
      </b-col>
    </b-container>
    <footer-bar />
  </div>
</template>

<script>
import NavBar from '~/components/Navigation/Navbar.vue'
import FooterBar from '~/components/Navigation/FooterBar.vue'
import SearchBox from '~/components/SearchBox.vue'

export default {
  components: {
    NavBar,
    FooterBar,
    	SearchBox
  },
  data () {
    return {
      searchQuery: ''
    }
  }
}
</script>

<style>
#search-box-container {
	margin: 1.5em 0;
}
</style>
