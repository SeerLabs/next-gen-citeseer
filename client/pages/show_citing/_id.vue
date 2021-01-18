<template>
    <!-- $ sudo sysctl fs.inotify.max_user_watches=524288
    $ sudo sysctl -p-->

    <div id="doc-view-layout">
        <!-- Main Info Row -->
        <v-row no-gutters>
            <v-col cols="12">
                <div class="d-flex">
                    <h2>What papers cite this paper. . .</h2>
                    <v-tooltip top>
                        <template v-slot:activator="{ on, attrs }">
                            <v-btn id="tooltip" icon v-bind="attrs" v-on="on">
                                <v-icon>help</v-icon>
                            </v-btn>
                        </template>
                        <span>You are seeing this page because the summary page is not indexed</span>
                    </v-tooltip>
                </div>
            </v-col>
        </v-row>
        <v-row id="abstract" no-gutters align-h="center">
            <v-col cols="12">
                <h1>{{ title }}</h1>
                <!-- <h5>{{ authors.join(', ')}}</h5> -->
                <h5>{{ venue }} - {{ year }}</h5>
                <br />
            </v-col>
        </v-row>

        <v-row id="citation-card" no-gutters class="citation-card" align-h="center">
            <v-col cols="12">
                <doc-results-container
                    v-model="sortBy"
                    :documents="documents"
                    :total-page-results="totalPageResults"
                    :page="page"
                    :sort-dropdown="sortDropdown"
                />
                <v-pagination
                    v-model="page"
                    :total-rows="totalPageResults"
                    :per-page="pageSize"
                    @input="getCiting()"
                />
            </v-col>
        </v-row>
        <!-- Citations Row -->
        <!-- <v-row id ="citation-card" class="citation-card" align-h="center">
                <v-col cols="12">
                    <citation-card id="citation-card" title="Citations" v-bind:doi="doi" v-bind:ncitation="nCitation"/>
                </v-col>
        </v-row>-->
    </div>
</template>

<script>
import ShowCitingService from '~/api/ShowCitingService';
import DocResultsContainer from '~/components/DocResults/DocResultsContainer.vue';

export default {
    components: {
        DocResultsContainer
    },

    data() {
        return {
            readMoreToggle: false,
            title: '',
            year: 0,
            authors: [],
            venue: '',
            abstract: '',
            nCitation: '',
            totalPageResults: 1000,
            documents: [],
            sortBy: 'yearAsc',
            sortDropdown: [
                {
                    text: 'Citation Count',
                    sortByKey: 'citCount'
                },
                {
                    text: 'Year (Ascending)',
                    sortByKey: 'yearAsc'
                },
                {
                    text: 'Year (Descending)',
                    sortByKey: 'yearDesc'
                }
            ],
            pageSize: 10,
            page: 1
        };
    },
    mounted() {
        this.getCiting();
    },
    methods: {
        getCiting() {
            ShowCitingService.getShowCiting(
                this.$route.params.id,
                this.page,
                this.pageSize,
                this.sortBy
            ).then((response) => {
                this.title = response.data.cluster.ctitle;
                this.year = response.data.cluster.cyear;
                this.authors = response.data.cluster.cauthors;
                this.venue = response.data.cluster.cvenue;
                this.documents = response.data.papers;
                this.totalPageResults = response.data.total_results;
            });

            if (!this.title) {
                this.title = 'Title Not Indexed';
            }
            if (!this.year || this.year === 0) {
                this.year = 'Year Not Indexed';
            }
            if (!this.authors) {
                this.authors = 'Authors Not Indexed';
            }
            if (!this.venue) {
                this.venue = 'Venue Not Indexed';
            }
        },
        alert() {
            window.alert(
                'You are seeing this page because the summary page is not indexed.'
            );
        }
    },
    layout: 'search'
};
</script>

<style>
#doc-view-layout {
    background: rgb(255, 255, 255);
}

#tooltip {
    margin-left: 3em;
}

#abstract {
    margin-top: 4%;
    margin-bottom: 2%;
    background: #ffffff;
}
#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
}

#pdf-btn {
    background: rgb(235, 0, 0);
    outline: transparent;
    border-color: transparent;
}

#toc {
    position: fixed;
    right: 5%;
    margin-top: 20%;
}
</style>
