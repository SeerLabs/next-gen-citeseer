<template>
    <div id="searchbox">
        <b-input-group prepend="All Fields" class="mt-3">
            <b-form-input
                v-model="searchQuery"
                value="Test"
                @input="handleInput"
            />
            <b-input-group-append>
                <b-button variant="info" type="submit" @click="submitInput">
                    Search
                </b-button>
            </b-input-group-append>
        </b-input-group>
    </div>
</template>

<script>
export default {
    name: 'SearchBox',
    props: {},
    data() {
        return {
            searchQuery: ''
        };
    },
    created() {
        this.searchQuery = this.$route.query.query || '';
    },
    methods: {
        handleInput() {
            this.$emit('input', this.searchQuery);
        },
        submitInput() {
            this.$router.push({
                name: 'search_result',
                query: { query: this.searchQuery }
            });
        }
    }
};
</script>

<style></style>
