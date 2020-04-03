<template>
  <div>
    <navbar/>
    <search-box/>
  </div>
</template>

<script>
import Navbar from '~/components/Navbar.vue'
import SearchBox from '~/components/SearchBox.vue'
export default {
    components: {
        Navbar,
        SearchBox
    }
}
</script>

<style>

</style>
