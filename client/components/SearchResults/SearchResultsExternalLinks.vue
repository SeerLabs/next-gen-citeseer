<template>
    <div id="search-results-external-links">
        <v-card :title="filter_title">
            <v-card-title>{{ filter_title }}</v-card-title>
            <v-card-text>
                LINKS
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
export default {
    name: 'SearchResultsExternalLinks',
    data() {
        return {
            filter_title: 'Try your query at'
        };
    }
};
</script>

<style scoped>
#search-results-external-links {
    margin-bottom: 10px;
}
</style>
