<template>
    <div id="searchbox">
        <template>
            <b-input-group prepend="All Fields" class="mt-3">
            <b-form-input></b-form-input>
                <b-input-group-append>
                    <b-button variant="info" v-on:click="getPaperResults">Search</b-button>
                </b-input-group-append>
            </b-input-group>
        </template>
        {{searchResults}}
    </div>
</template>

<script>
    import SearchPaperService from '../api/SearchPaperService'
    export default {
        name: 'SearchBox',
        data () {
                return {
                    searchResults: null
                }
            },
        methods: {
            async getPaperResults () {
                SearchPaperService.searchPaper()
                .then(response => (this.searchResults = response.data))
            }
        }
    }
</script>
<style>
</style>
