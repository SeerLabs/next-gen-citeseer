<template>
    <v-autocomplete
        v-model="searchQuery"
        :items="items"
        :loading="isLoading"
        :search-input.sync="textInput"
        filled
        clearable
        hide-no-data
        hide-selected
        item-text="Description"
        item-value="API"
        placeholder="Search"
        @keyup.enter="submitInput"
    >
        <template v-slot:append>
            <div id="search-button" @click="submitInput">
                <v-icon class="ml-3">search</v-icon>
            </div>
        </template>
    </v-autocomplete>
</template>

<script>
import searchPaperService from '~/api/SearchPaperService';

export default {
    name: 'SearchBox',
    props: {},
    data() {
        return {
            descriptionLimit: 60,
            searchQuery: '',
            textInput: '',
            entries: [],
            isLoading: false
        };
    },
    computed: {
        items() {
            return this.entries.map((entry) => {
                const Description =
                    entry.length > this.descriptionLimit
                        ? entry.slice(0, this.descriptionLimit) + '...'
                        : entry;

                return Object.assign({}, entry, { Description });
            });
        }
    },
    watch: {
        textInput(val) {
            if (val == null) {
                return;
            }
            this.isLoading = true;
            console.log(this.textInput);

            searchPaperService
                .getSuggestions(this.textInput)
                .then((response) => {
                    console.log(response);
                    this.entries = response.data.suggestions.map(
                        (suggestion) => suggestion.text
                    );
                    console.log(this.entries);
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                })
                .finally(() => {
                    this.isLoading = false;
                });
        }
    },
    created() {
        console.log(this.$route.query.query);
        this.textInput = this.$route.query.query || '';
    },
    methods: {
        submitInput() {
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
