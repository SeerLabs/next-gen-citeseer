<template>
	<v-footer app padless absolute color="tertiary" class="pa-15">
		<v-row justify="start" no-gutters>
      <v-col cols="3" align-self="center" class="mr-3">
        <img id="ist-logo" src="@/assets/img/ist_logo.svg" alt="Hosted by Penn State College of IST">
      </v-col>
      <v-col cols="2">
        <ul>
          <h4 class="secondary--text pb-3">Information</h4>
          <li><a href="#">About CiteSeerX</a></li>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Data</a></li>
          <li><a href="#">Source</a></li>
        </ul>
      </v-col>
      <v-col cols="2">
        <ul>
          <h4 class="secondary--text pb-3">Service</h4>
          <li><a href="#">Submit Documents</a></li>
          <li><a href="#">Help</a></li>
          <li><a href="#">Contact Us</a></li>
        </ul>
      </v-col>
      <v-col cols="5">

      </v-col>
    </v-row>
	</v-footer>
</template>

<script>
export default {

}
</script>

<style scoped>

  ul {
    list-style-type: none;
  }

  a:link,
  a:visited,
  a:active {
    text-decoration: none;
    color: var(--v-secondary-base);
    font-size: 0.7em;
  }

  a:hover {
    color: var(--v-primary-base);
  }

  #ist-logo {
    width: 15em;
  }

</style>
