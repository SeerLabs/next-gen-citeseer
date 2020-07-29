<template>
    <div>
        <v-card>
            <v-card-title>{{ title }}</v-card-title>
            <v-card-text>
                <v-select
                    dense
                    class="m-2"
                    :value="sortByValues[0]"
                    :items="sortByValues"
                    label="Sort By"
                    outlined
                />
                <v-simple-table striped hover :items="items">
                    <template v-slot:default>
                        <thead>
                            <tr>
                                <th class="text-left">Datum</th>
                                <th class="text-left">Value</th>
                                <th class="text-left">Source</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(item, index) in items" :key="index">
                                <td>{{ item.Datum }}</td>
                                <td>{{ item.Value }}</td>
                                <td>{{ item.Source }}</td>
                            </tr>
                        </tbody>
                    </template>
                </v-simple-table>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
export default {
    name: 'VersionHistoryCard',
    components: {},
    props: {
        title: { type: String, default: '' },
        cardType: { type: String, default: '' }
    },
    data() {
        return {
            sortByValues: ['Version 1', 'Version 2', 'Version 3'],
            items: [
                {
                    Datum: 'TITLE',
                    Value: 'On clustering techniques of citation graphs',
                    Source: 'INFERENCE'
                },
                {
                    Datum: 'AUTHOR NAME',
                    Value: 'F. P. Preparata',
                    Source: 'SVM HeaderParse 0.2'
                },
                {
                    Datum: 'AUTHOR NAME',
                    Value: 'R. T. Chien',
                    Source: 'SVM HeaderParse 0.2'
                },
                {
                    Datum: 'ABSTRACT',
                    Value:
                        'Distribution of this report is unlimited. Qualified requesters',
                    Source: 'SVM HeaderParse 0.2'
                },
                { Datum: 'YEAR', Value: '1967', Source: 'INFERENCE' },
                {
                    Datum: 'VENUE TYPE',
                    Value: 'TECHREPORT',
                    Source: 'INFERENCE'
                },
                { Datum: 'TECH', Value: 'Report R349', Source: 'INFERENCE' },
                { Datum: 'CITATIONS', Value: '6 found', Source: 'ParsCit 1.0' }
            ]
        };
    }
};
</script>

<style></style>>
