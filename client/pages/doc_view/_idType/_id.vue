<template>
    <div v-cloak id="doc-view-layout">
        <div v-if="loading" id="loading">
            <v-progress-linear rounded indeterminate color="teal" />
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
            <v-row>
                <v-col cols="9">
                    <citation-card
                        id="citations"
                        class="citation-card"
                        :doc-id="docId"
                        :cid="cid"
                        title="Citations"
                    />

                    <citation-card
                        id="similar-articles"
                        class="citation-card"
                        :doc-id="docId"
                        :cid="cid"
                        title="Similar Articles"
                    />
                    <version-history-card
                        id="version-history"
                        title="Version History"
                    />
                </v-col>
                <v-col cols="3">
                    <v-card id="table-of-contents">
                        <v-card-title>Table of Contents</v-card-title>
                        <v-card-text>
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
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </span>
    </div>
</template>

<script>
import $ from 'jquery';

import { mapActions } from 'vuex';
import DocumentViewHeader from '~/components/DocView/DocumentViewHeader.vue';
import CitationCard from '~/components/DocView/CitationCard.vue';
import VersionHistoryCard from '~/components/DocView/VersionHistoryCard.vue';

export default {
    components: {
        DocumentViewHeader,
        CitationCard,
        VersionHistoryCard
    },
    async fetch() {
      // const res = await axios.get('https://facebook.com');
      // console.log(res);
    },
    data() {
        return {
            loading: false,
            showAbstract: false,
            docId: this.$route.params.id,
            idType: this.$route.params.idType,
            cid: '',
            title: '',
            year: '',
            authors: [],
            venue: '',
            abstract: '',
            nCitations: 0,

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
    async created() {
        this.loading = true;
        let data = null;
        switch (this.idType){
            case 'pid':
                data = await this.getPaperWithPaperId({pid: this.docId});
                break;
            case 'cid':
                data = await this.getPaperWithClusterId({cid: this.docId});
                // set docID from cluster id back to paper id
                this.docId = data.paper.id
                break;
            default:
                this.loading = false;
                return;
        }
        this.cid = data.paper.cluster_id
        this.title = data.paper.title;
        this.year = data.paper.year;
        this.authors = data.paper.authors;
        this.venue = data.paper.venue;
        this.abstract = data.paper.abstract;
        this.nCitation = data.paper.n_citation;

        this.loading = false;
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
        ...mapActions(['getPaperWithPaperId', 'getPaperWithClusterId']),

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
    padding: 50px 0;
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

[v-cloak] {
    display: none;
}
</style>
