<template>
  <div>
    <b-card v-bind:title="title" v-bind:sub-title="ncitation">
      <b-row>
        <b-col>
          <div class="document-results-sorting">
            Sort by
            <b-dropdown variant="primary" class="m-2 results-dropdown">
              <template v-slot:button-content>
                {{ sortByDisplay }}
              </template>

              <ul>
                <li v-for="(item, key) in sortDropdown" :key="key">
                  <b-dropdown-item :name="key" v-on:click="sortResults">
                    {{ item.displayName }}
                  </b-dropdown-item>
                </li>
              </ul>
            </b-dropdown>
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <citation-list doi="doi" v-bind:type="title" />
        </b-col>
      </b-row>

      <!-- <b-card-text>
            Some quick example text to build on the <em>card title</em> and make up the bulk of the card's
            content.
            </b-card-text>

            <b-card-text>A second paragraph of text in the card.</b-card-text> -->

      <!-- <a href="#" class="card-link">Card link</a>
            <b-link href="#" class="card-link">Another link</b-link> -->
    </b-card>
  </div>
</template>

<script>
import CitationList from "~/components/DocumentView/CitationList.vue";
export default {
  name: "CitationCard",
  components: {
    CitationList
  },
  props: {
    doi: String,
    title: String,
    ncitation: Number
  },
  data() {
    return {
      sortByDisplay: "",
      sortDropdown: {},
      sortByKey: ""
    };
  },
  methods: {
    sortResults: function(event) {
      console.log(event);
      const dropdownItem = event.target.name;
      this.sortByDisplay = event.target.text;
      this.sortByKey = this.sortDropdown[dropdownItem].sortByKey;
    }
  },
  mounted() {
    switch (this.title) {
      case "Citations":
        this.sortByDisplay = "Relevance";
        this.sortDropdown = {
          "sort-relevance": {
            displayName: "Relevance",
            sortByKey: "relevance"
          },
          "sort-Recency": { displayName: "Recency", sortByKey: "Recency" }
        };
        this.sortByKey = "relevance";
        break;
      case "Similar Articles":
        this.sortByDisplay = "Co-Citation";
        this.sortDropdown = {
          "sort-co-citation": {
            displayName: "Co-Citation",
            sortByKey: "co-citation"
          },
          "sort-active-bibliography": {
            displayName: "Active Bibliography",
            sortByKey: "active-bibliography"
          }
        };
        this.sortByKey = "co-citation";
        break;
    }
  }
};
</script>

<style scoped>
.document-results-sorting {
  text-align: right;
}

.results-dropdown li {
  list-style: none;
}

.results-dropdown ul {
  padding: 0;
}
</style>
