<template>
    <div id="searchbox">
        <b-form @submit.prevent="submitInput">
            <b-input-group prepend="All Fields" class="mt-3">
                <b-form-input v-model="searchQuery" @input="handleInput"></b-form-input>

                <b-input-group-append>
                    <b-button variant="info" type="submit">Search</b-button>
                </b-input-group-append>
            </b-input-group>
        </b-form>
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
                this.$emit('submit', this.searchQuery);
            }
        }
    }
</script>

<style>
</style>
