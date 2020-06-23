<template>
    <div id="searchbox">
        <b-input-group prepend="All Fields" class="mt-3">
            <b-form-input v-model="searchQuery" @input="handleInput"></b-form-input>
            <b-input-group-append>
                <b-button variant="info" type="submit" @click="submitInput">Search</b-button>
            </b-input-group-append>
        </b-input-group>
    </div>
</template>

<script>
    // @TODO direct search bar to the search results page
    import SearchPaperService from '../api/SearchPaperService'
    export default {
        name: 'SearchBox',
        props: {
        },
        data() {
            return {
                searchQuery: ""
            }
        },
        methods: {
            handleInput() {
                this.$emit('input', this.searchQuery);
            },
            submitInput() {
                console.log(this.searchQuery);
                this.$router.push({ name: 'search_result', query: { query: this.searchQuery }});
            },
        }
    }
</script>

<style>
</style>
