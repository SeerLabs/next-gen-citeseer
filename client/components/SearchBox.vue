<template>
    <v-combobox
        v-model="searchQuery"
        :items="items"
        :loading="isLoading"
        :search-input.sync="textInput"
        filled
        clearable
        hide-no-data
        hide-selected
        item-text="description"
        item-value="title"
        placeholder="Search"
        @keydown.enter="submitInput"
    >
        <template v-slot:append>
            <div id="search-button" @click="submitInput">
                <v-icon class="ml-3">search</v-icon>
            </div>
        </template>
    </v-combobox>
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

                return { title: entry, description: Description };
            });
        }
    },
    watch: {
        textInput(val) {
            // Items have already been requested
            if (this.textInput === this.searchQuery) return;

            if (this.isLoading) return;

            this.isLoading = true;

            searchPaperService
                .getSuggestions(this.textInput)
                .then((response) => {
                    console.log(response);
                    this.entries = response.data.suggestions.map(
                        (suggestion) => suggestion.text
                    );
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                })
                .finally(() => (this.isLoading = false));
        },
        searchQuery() {
            // Note, item-value is currently not working on v-combobox as a known issue with Vuetify
            // As a workaround, we check to make sure that the searchQuery exists before pulling its value
            this.textInput = this.searchQuery ? this.searchQuery.title : '';
            this.submitInput();
        }
    },
    created() {
        this.textInput = this.$route.query.query || '';
        this.searchQuery = this.textInput;
    },
    methods: {
        submitInput() {
            if (this.textInput) {
                this.entries = [];

                this.$router.push({
                    name: 'search_result',
                    query: { query: this.textInput }
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
