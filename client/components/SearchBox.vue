<template>
    <v-card flat>
      <v-combobox
          v-model="searchQuery"
          class="mb-0 pb-0"
          :items="items"
          :loading="isLoading"
          :search-input.sync="textInput"
          :hide-no-data="!textInput"
          filled
          clearable
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
      <v-container
        class="pa-0"
        fluid
      >
        <v-checkbox 
          id="pdf-checkbox"
          v-model="includeWithoutPdfs"
          class="pt-0 mt-0"
          dense
          label="Include results without PDF"
          @click="submitInput"
        />
      </v-container>
    </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'SearchBox',
    props: {},
    data() {
        return {
            descriptionLimit: 60,
            searchQuery: '',
            textInput: '',
            entries: [],
            isLoading: false,
            includeWithoutPdfs: false
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
        textInput() {
            // Items have already been requested
            if (this.textInput === this.searchQuery) return;
            if (this.isLoading) return;

            if (this.textInput) {
              this.isLoading = true;
              
              this.getSuggestions({queryString: this.textInput})
                  .then((response) => {
                      this.entries = response.suggestions;
                  })
                  .finally(() => (this.isLoading = false));
            }
        },
        searchQuery() {
            if (this.searchQuery && this.searchQuery.type) {
                const idType =
                    this.searchQuery.type === 'paper' ? 'cid' : 'pid';

                this.$router.push({
                    name: 'doc_view-idType-id',
                    params: { idType, id: this.searchQuery.id }
                });
            }
        }
    },
    created() {
        this.textInput = this.$route.query.query || '';
        this.includeWithoutPdfs = this.$route.query.pdf != null && !this.$route.query.pdf || false;
        this.searchQuery = this.textInput;
    },
    methods: {
        ...mapActions(['getSuggestions']),
        submitInput() {
            if (this.textInput) {
                this.entries = [];

                this.$router.push({
                    name: 'search_result',
                    query: {
                        query: this.textInput,
                        pdf: !this.includeWithoutPdfs
                    }
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

<style>
.v-label {
  margin-bottom: 0 !important;
}
</style>