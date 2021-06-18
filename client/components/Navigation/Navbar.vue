<template>
    <header>
        <v-app-bar id="navbar" dark>
            <v-toolbar-title href="#">
                <nuxt-link id="navbar-home-link" :to="{ path: '/' }">
                    CiteSeerX
                </nuxt-link>
            </v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn text href="#">Profile</v-btn>
            <v-btn text href="#">Sign Out</v-btn>
        </v-app-bar>
    </header>
</template>

<style scoped>
header {
    margin-bottom: 1.5em;
}

#navbar-home-link {
    color: inherit;
    text-decoration: none;
}
</style>
