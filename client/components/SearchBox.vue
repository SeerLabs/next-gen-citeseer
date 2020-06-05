<template>
    <div id="searchbox">
        <b-form @submit.prevent="$emit('submit', $event.target.value)">
            <b-input-group prepend="All Fields" class="mt-3">
            <b-form-input v-model="queryString" required></b-form-input>
                <b-input-group-append>
                    <b-button variant="info" type="submit">Search</b-button>
                </b-input-group-append>
            </b-input-group>
        </b-form>
    </div>
</template>

<script>
    import SearchPaperService from '../api/SearchPaperService'
    export default {
        name: 'SearchBox',
        data() {
            return {
                queryString: '',
            }
        },
    }
</script>
<style>
</style>
