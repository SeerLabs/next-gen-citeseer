<template>
    <div class="overflow-auto">
        <b-table
            id="my-table"
            thead-class="hidden_header"
            :items="items"
            :per-page="perPage"
            :current-page="currentPage"
            small
        ></b-table>

        <b-pagination
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
            aria-controls="my-table"
        ></b-pagination>

        <!-- <p class="mt-3">Current Page: {{ currentPage }}</p> -->
    </div>
</template>

<script>
    export default {
        name: 'CitationCard',
        data() {
            return {
                perPage: 3,
                currentPage: 1,
                items: [
                    {title: 'Place Holder For Paper Titile Here 1', author: "author 1", year: "year 1"},
                    {title: 'Place Holder For Paper Titile Here 2', author: "author 2", year: "year 2"},
                    {title: 'Place Holder For Paper Titile Here 3', author: "author 3", year: "year 3"},
                    {title: 'Place Holder For Paper Titile Here 4', author: "author 4", year: "year 4"},
                    {title: 'Place Holder For Paper Titile Here 5', author: "author 5", year: "year 5"},
                    {title: 'Place Holder For Paper Titile Here 6', author: "author 6", year: "year 6"},
                    {title: 'Place Holder For Paper Titile Here 7', author: "author 7", year: "year 7"},
                    {title: 'Place Holder For Paper Titile Here 8', author: "author 8", year: "year 8"},
                    {title: 'Place Holder For Paper Titile Here 9', author: "author 9", year: "year 9"}
                ]
            }
        },
        computed: {
            rows() {
                return this.items.length
            }
        }
    }
</script>
<style>
.hidden_header {
  display: none;
}
</style>