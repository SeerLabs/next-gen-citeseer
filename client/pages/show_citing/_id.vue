<template>
    <!-- $ sudo sysctl fs.inotify.max_user_watches=524288
    $ sudo sysctl -p-->

    <div id="doc-view-layout">
        <!-- Main Info Row -->
        <b-row>
            <b-col cols="5">
                <h2>What papers cite this paper. . .</h2>
            </b-col>
            <b-col>
                <b-button
                    v-b-tooltip.hover
                    title="You are seeing this page because the summary page is not indexed"
                    size="sm"
                    pill
                    variant="outline-secondary"
                >
                    ?
                </b-button>
            </b-col>
        </b-row>
        <b-row id="abstract" align-h="center">
            <b-col cols="9">
                <h1>{{ title }}</h1>
                <!-- <h5>{{ authors.join(', ')}}</h5> -->
                <h5>{{ venue }} - {{ year }}</h5>
                <br />
            </b-col>
        </b-row>

        <b-row id="citation-card" class="citation-card" align-h="center">
            <b-col cols="12">
                <doc-results-container
                    v-model="sortBy"
                    :documents="documents"
                    :total-page-results="totalPageResults"
                    :page="page"
                    :sort-dropdown="sortDropdown"
                />
                <b-pagination
                    v-model="page"
                    :total-rows="totalPageResults"
                    :per-page="pageSize"
                    @input="getCiting()"
                />
            </b-col>
        </b-row>
        <!-- Citations Row -->
        <!-- <b-row id ="citation-card" class="citation-card" align-h="center">
                <b-col cols="12">
                    <citation-card id="citation-card" title="Citations" v-bind:doi="doi" v-bind:ncitation="nCitation"/>
                </b-col>
        </b-row>-->
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
            sortDropdown: {
                citCount: {
                    displayName: 'Citation Count',
                    sortByKey: 'citCount'
                },
                yearAsc: {
                    displayName: 'Year (Ascending)',
                    sortByKey: 'yearAsc'
                },
                yearDesc: {
                    displayName: 'Year (Descending)',
                    sortByKey: 'yearDesc'
                }
            },
            pageSize: 10,
            page: 1
        };
    },
    watch: {
        sortBy() {
            this.getCiting();
        }
    },
    mounted() {
        this.getCiting();
    },
    methods: {
        getCiting() {
            console.log(this.$route.params);

            ShowCitingService.getShowCiting(
                this.$route.params.id,
                this.page,
                this.pageSize,
                this.sortBy
            ).then(response => {
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
    layout: 'layout_search'
};
</script>

<style>
#doc-view-layout {
    background: rgb(255, 255, 255);
}
#side-margine {
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
