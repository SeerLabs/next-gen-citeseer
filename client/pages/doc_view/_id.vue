<template>
    <div id="doc-view-layout">
        <div v-if="loading" id="loading">
            <b-spinner label="Spinning" />
        </div>
        <span v-else>
            <DocumentViewHeader
                :title="title"
                :abstract="abstract"
                :year="year"
                :authors="authors"
                :venue="venue"
                :n-citation="nCitation"
                :doc-id="docId"
            />

            <!-- Citations Row -->
            <b-row>
                <b-col cols="9">
                    <citation-card
                        id="citations"
                        class="citation-card"
                        :doc-id="docId"
                        title="Citations"
                        :ncitation="nCitation"
                    />

                    <citation-card
                        id="similar-articles"
                        class="citation-card"
                        :doc-id="docId"
                        title="Similar Articles"
                        citation
                    />
                    <version-history-card
                        id="version-history"
                        title="Version History"
                    />
                </b-col>
                <b-col cols="3">
                    <b-card id="table-of-contents" title="Table of Contents">
                        <b-card-text>
                            <a href="#citations">
                                <h6>Citation</h6>
                            </a>
                            <a
                                href="#similar-articles"
                                @click="scroll('similar-article-card')"
                            >
                                <h6>Similar Articles</h6>
                            </a>
                            <a href="#version-history">
                                <h6>Version History</h6>
                            </a>
                        </b-card-text>
                    </b-card>
                </b-col>
            </b-row>
        </span>
    </div>
</template>

<script>
import $ from 'jquery';
import DocumentViewHeader from '~/components/DocView/DocumentViewHeader.vue';
import CitationCard from '~/components/DocView/CitationCard.vue';
import DocViewService from '~/api/DocViewService';
import VersionHistoryCard from '~/components/DocView/VersionHistoryCard.vue';

export default {
    components: {
        DocumentViewHeader,
        CitationCard,
        VersionHistoryCard
    },
    async fetch() {
        this.loading = true;
        const { data } = await DocViewService.getPaperEntity(this.docId);

        this.title = data.paper.title;
        this.year = data.paper.year;
        this.authors = data.paper.authors;
        this.venue = data.paper.venue;
        this.abstract = data.paper.abstract;
        this.nCitation = data.paper.total_results;

        this.loading = false;
    },
    data() {
        return {
            loading: false,
            showAbstract: false,
            docId: this.$route.params.id,
            title: '',
            year: '',
            authors: [],
            venue: '',
            abstract: '',
            nCitation: 0,

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
    computed: {
        getPDFUrl() {
            return '/pdf/' + this.docId;
        }
    },
    mounted() {
        $('#table-of-contents a').on('click', function(e) {
            e.preventDefault();
            const hash = this.hash;

            // animate
            $('html, body').animate(
                {
                    scrollTop: $(hash).offset().top
                },
                300,
                function() {
                    window.location.hash = hash;
                }
            );
        });
    },
    methods: {
        toggleReadMore() {
            this.readMoreFlag = true;
        },
        scroll(id) {
            return null;
            // document.getElementById(id).scrollIntoView();
        }
    },
    layout: 'layout_search'
};
</script>

<style>
#loading {
    text-align: center;
    padding: 50px;
}
#doc-view-layout {
    background: rgb(255, 255, 255);
}

.citation-card {
    margin-bottom: 1em;
}

#table-of-contents {
    position: sticky;
    top: 5em;
}

#table-of-contents .card-body {
    padding: 1rem;
}
</style>
