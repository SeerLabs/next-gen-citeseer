<template>
    <v-app-bar id="navbar" flat app color="primary" class="no-text-transform">
        <v-toolbar-title href="#">
            <nuxt-link id="navbar-home-link" :to="{ path: '/' }">
                CiteSeerX
            </nuxt-link>
        </v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn text href="#" class="secondary--text font-weight-bold">About</v-btn>
        <v-btn text href="#" class="secondary--text font-weight-bold">Submit</v-btn>
        <v-btn text href="#" class="secondary--text font-weight-bold">DMCA</v-btn>
        <v-btn text href="#" class="secondary--text font-weight-bold">Donate</v-btn>
        <v-btn text href="#" class="secondary--text font-weight-bold">MyCiteSeerX</v-btn>
    </v-app-bar>
</template>

<style scoped>

#navbar-home-link {
    color: #ffffff;
    text-decoration: none;
}

</style>
