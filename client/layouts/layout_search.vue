<template>
  <div>
	<nav-bar/>
	<b-container fluid="md">
		<b-col cols="12" id="page-container">
			<b-row>
				<b-col sm="8" id="search-box-container">
					<search-box/>
				</b-col>
			</b-row>
			<nuxt/>
		</b-col>
	</b-container>
	<footer-bar/>
  </div>
</template>


<script>
import NavBar from '~/components/Navigation/NavBar.vue';
import FooterBar from '~/components/Navigation/FooterBar.vue';
import SearchBox from '~/components/SearchBox.vue'

export default {
	components: {
		NavBar,
		FooterBar,
    	SearchBox
	}
};
</script>


<style>
#search-box-container {
	margin: 1.5em 0;
}
</style>
