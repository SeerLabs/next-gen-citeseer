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
            return this.entries.map(({ type, text, id }) => {
                const Description =
                    text.length > this.descriptionLimit
                        ? text.slice(0, this.descriptionLimit) + '...'
                        : text;

                return { type, text, id, description: Description };
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
                    this.entries = response.data.suggestions;
                })
                .catch((error) => {
                    // eslint-disable-next-line
                    console.log(error.message);
                    this.error = true;
                })
                .finally(() => (this.isLoading = false));
        },
        searchQuery() {
            const idType = this.searchQuery.type === 'paper' ? 'pid' : 'cid';

            this.$router.push({
                name: 'doc_view-idType-id',
                params: { idType, id: this.searchQuery.id }
            });
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
