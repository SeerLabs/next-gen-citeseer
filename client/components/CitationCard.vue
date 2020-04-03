<template>
    <div>
        <b-card v-bind:title="title" v-bind:sub-title="ncitation">
            <citation-list/>

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
    import CitationList from './CitationList.vue'
    export default {
        name: 'CitationCard',
        components: {
            CitationList
        },
        props: ['title', 'ncitation']
    }
</script>

<style>
</style>