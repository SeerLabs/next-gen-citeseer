<template>
    <layout-default>
        <v-container class="pt-10">
            <v-row>
                <v-col cols="8">
                    <search-box v-model="searchQuery" />
                </v-col>
            </v-row>
        </v-container>

        
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

[v-cloak] {
    display: none;
}
</style>
