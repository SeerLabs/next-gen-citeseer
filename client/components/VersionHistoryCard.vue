<template>
    <div>
        <b-card v-bind:title="title">
            <b-dropdown text="Versions" variant="outline-secondary" class="m-md-2" size="sm">
                                <b-dropdown-item>Version 1</b-dropdown-item>
                                <b-dropdown-item>Version 2</b-dropdown-item>
                                <b-dropdown-item>Version 3</b-dropdown-item>
                            </b-dropdown>

            <b-table striped hover :items="items"></b-table>

        </b-card>
    </div>
</template>

<script>
    export default {
        name: 'VersionHistoryCard',
        components: {
        },
        props: ['title', 'card_type'],
        data() {
            return {
                items: [
                    { Datum: 'TITLE', Value: 'On clustering techniques of citation graphs', Source: 'INFERENCE' },
                    { Datum: 'AUTHOR NAME', Value: 'F. P. Preparata', Source: 'SVM HeaderParse 0.2' },
                    { Datum: 'AUTHOR NAME', Value: 'R. T. Chien', Source: 'SVM HeaderParse 0.2' },
                    { Datum: 'ABSTRACT', Value: 'Distribution of this report is unlimited. Qualified requesters', Source: 'SVM HeaderParse 0.2' },
                    { Datum: 'YEAR', Value: '1967', Source: 'INFERENCE' },
                    { Datum: 'VENUE TYPE', Value: 'TECHREPORT', Source: 'INFERENCE' },
                    { Datum: 'TECH', Value: 'Report R349', Source: 'INFERENCE' },
                    { Datum: 'CITATIONS', Value: '6 found', Source: 'ParsCit 1.0' }
                ]
            }
        }
    }
</script>

<style>
    
</style>>