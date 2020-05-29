<template>
  <div>
	<nav-bar/>
	<b-container fluid="md">
		<b-row>
			<b-col cols="12" id="page-container">
    			<nuxt/>
			</b-col>
		</b-row>
	</b-container>
	<footer-bar/>
  </div>
</template>


<script>
import NavBar from '~/components/Navigation/NavBar.vue';
import FooterBar from '~/components/Navigation/FooterBar.vue';

export default {
	name: 'LayoutDefault',
	components: {
		NavBar,
		FooterBar
	}
};
</script>


<style>
	#page-container {
		margin: auto;
	}
</style>
