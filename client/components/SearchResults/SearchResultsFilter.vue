<template>
    <v-card id="search-results-filter" :title="filter_title">
        <v-card-title>{{ filter_title }}</v-card-title>
        <v-card-text>
            <div class="d-flex justify-space-between">
                <label for="year-filter">Year</label>
                <span>1999 - {{ value }}</span>
            </div>
            <v-row>
                <v-col cols="12">
                    <v-form-input
                        id="year-filter"
                        v-model="value"
                        type="range"
                        min="1999"
                        max="2020"
                    />
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>

<script>
export default {
    name: 'SearchResultsFilter',
    data() {
        return {
            filter_title: 'Filter results',
            value: 2020
        };
    }
};
</script>

<style scoped>
#search-results-filter {
    margin-bottom: 20px;
}

#year-filter-value {
    text-align: right;
}
</style>
