<template>
    <!-- $ sudo sysctl fs.inotify.max_user_watches=524288
    $ sudo sysctl -p-->

    <div id="doc-view-layout">
        <b-container fluid>
            <!-- Main Info Row -->
            <b-row id="doc-view-top">
                <b-col cols="9">
                    <h2>{{ title }}</h2>
                    <h5>{{ authors.join(', ') }}</h5>
                    <h5>{{ venue }} - {{ year }}</h5>
                    <br />

                    <div
                        id="abstract"
                        :style="
                            showAbstract
                                ? { height: 'min-content' }
                                : { height: '150px' }
                        "
                    >
                        <p>{{ abstract }}</p>
                    </div>

                    <b-button
                        @click="() => (showAbstract = !showAbstract)"
                    >{{ !showAbstract ? 'Show more' : 'Show less' }}</b-button>
                </b-col>
                <b-col cols="3">
                    <b-card id="document-options">
                        <b-card-text>
                            <!-- PDF Button -->
                            <b-button
                                squared
                                id="pdf-btn"
                                v-bind:to="getPDFUrl"
                                target="_blank"
                                class="mb-md-2"
                            >View PDF</b-button>

                            <!-- Download Links Drop Down -->
                            <b-dropdown
                                id="download-links-dropdown"
                                text="Download Links"
                                variant="outline-secondary"
                                class="mb-md-4"
                                size="sm"
                            >
                                <b-dropdown-item>Link 1</b-dropdown-item>
                                <b-dropdown-item>Link 2</b-dropdown-item>
                                <b-dropdown-item>Link 3</b-dropdown-item>
                            </b-dropdown>
                            <h6>Cite This</h6>
                            <h6>Save</h6>
                            <h6>Add to Collection</h6>
                            <h6>Add to MetaCart</h6>
                            <h6>Correct Errors</h6>
                        </b-card-text>
                    </b-card>
                </b-col>
            </b-row>

            <!-- Citations Row -->
            <b-row>
                <b-col cols="9">
                    <citation-card
                        class="citation-card"
                        id="citations"
                        title="Citations"
                        v-bind:ncitation="nCitation"
                    />

                    <citation-card
                        class="citation-card"
                        id="similar-articles"
                        title="Similar Articles"
                        citation
                    />
                    <version-history-card id="version-history" title="Version History" />
                </b-col>
                <b-col cols="3">
                    <b-card id="table-of-contents" title="Table of Contents">
                        <b-card-text>
                            <a href="#citations">
                                <h6>Citation</h6>
                            </a>
                            <a href="#similar-articles" v-on:click="scroll('similar-article-card')">
                                <h6>Similar Articles</h6>
                            </a>
                            <a href="#version-history">
                                <h6>Version History</h6>
                            </a>
                        </b-card-text>
                    </b-card>
                </b-col>
            </b-row>
        </b-container>
    </div>
</template>

<script>
import Navbar from '~/components/Navbar.vue';
import TableOfContent from '~/components/DocumentView/TableOfContent.vue';
import SearchBox from '~/components/SearchBox.vue';
import CitationCard from '~/components/DocumentView/CitationCard.vue';
import BaseCard from '~/components/Base/BaseCard.vue';
import DocViewService from '~/api/DocViewService';
import DocumentResultsList from '~/components/DocumentResults/DocumentResultsList.vue';
import VersionHistoryCard from '~/components/DocumentView/VersionHistoryCard.vue';

import $ from 'jquery';

export default {
    components: {
        Navbar,
        TableOfContent,
        SearchBox,
        CitationCard,
        BaseCard,
        DocumentResultsList,
        VersionHistoryCard
    },
    methods: {
        toggleReadMore: function () {
            this.readMoreFlag = true;
        },
        scroll: function (id) {
            return null;
            // document.getElementById(id).scrollIntoView();
        }
    },
    data() {
        return {
            showAbstract: false,
            title: '',
            year: '',
            authors: [],
            venue: '',
            abstract: '',
            nCitation: '',

            documents: [
                {
                    title: 'Document Title',
                    type: 'DOCUMENT',
                    authors: 'Abcdefg Lastname',
                    year: '2018',
                    abstract: 'Lorem ipsum',
                    numCitations: 20
                },
                {
                    title: 'ABCDEFG',
                    type: 'DOCUMENT',
                    authors: 'Hijklmno Pqrstuv',
                    year: '2020',
                    abstract: 'Lorem ipsum',
                    numCitations: 3
                },
                {
                    title: 'EFGHIJK',
                    type: 'CITATION',
                    authors: 'Firstname Lastname',
                    year: '2021',
                    abstract: 'Lorem ipsum',
                    numCitations: 30
                }
            ],
            totalPageResults: 1000
        };
    },
    mounted: function () {
        $('#table-of-contents a').on('click', function (e) {
            console.log('Press');
            e.preventDefault();

            var hash = this.hash;
            console.log(hash);

            // animate
            $('html, body').animate(
                {
                    scrollTop: $(hash).offset().top
                },
                300,
                function () {
                    window.location.hash = hash;
                }
            );
        });
    },
    async fetch() {
        const { data } = await DocViewService.getPaperEntity(
            this.$route.params.id
        );

        (this.title = data.paper.title),
            (this.year = data.paper.year),
            (this.authors = data.paper.authors),
            (this.venue = data.paper.venue),
            (this.abstract = data.paper.abstract),
            (this.nCitation = data.paper.total_results);
    },
    computed: {
        getPDFUrl() {
            return '/pdf/' + this.$route.params.id;
        }
    },
    layout: 'layout_search'
};
</script>

<style>
#doc-view-layout {
    background: rgb(255, 255, 255);
}

#doc-view-top {
    margin-top: 3em;
    margin-bottom: 3em;
    background: #ffffff;
}

#abstract {
    overflow: hidden;
}

#summary-text {
    padding-top: 2%;
    padding-bottom: 2%;
}

.citation-card {
    margin-bottom: 1em;
}

#pdf-btn {
    background: rgb(235, 0, 0);
    outline: transparent;
    border-color: transparent;
}

#table-of-contents {
    position: sticky;
    top: 5em;
}

#table-of-contents .card-body {
    padding: 1rem;
}
</style>
