<template>
    <v-text-field
        v-model="searchQuery"
        placeholder="Search"
        filled
        clearable
        type="text"
        @keyup.enter="submitInput"
    >
        <template v-slot:append>
            <div id="search-button" @click="submitInput">
                <v-icon class="ml-3">
                    search
                </v-icon>
            </div>
        </template>
    </v-text-field>
</template>

<script>
export default {
    name: 'SearchBox',
    props: {},
    data: function() {
        return {
            searchQuery: ''
        };
    },
    created: function() {
        this.searchQuery = this.$route.query.query || '';
    },
    methods: {
        submitInput: function() {
            if (this.searchQuery) {
                this.$router.push({
                    name: 'search_result',
                    query: { query: this.searchQuery }
                });
            }
        }
    }
};
</script>

<style scoped>
#search-button {
    cursor: pointer;
}
</style>
