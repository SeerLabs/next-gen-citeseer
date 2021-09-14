<template>
    <layout-default>
        <v-row>
            <v-col id="search-box-container" cols="8">
                <search-box v-model="searchQuery" />
            </v-col>
        </v-row>
        <nuxt keep-alive />
    </layout-default>
</template>

<script>
import LayoutDefault from './default.vue';
import SearchBox from '~/components/SearchBox.vue';

export default {
    components: {
      LayoutDefault,
      SearchBox
    },
    data() {
        return {
            searchQuery: ''
        };
    },
};
</script>

<style>

#search-box-container {
    margin: 1.5em 0;
}

[v-cloak] {
    display: none;
}
</style>
