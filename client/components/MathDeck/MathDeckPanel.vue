<template>

    <v-card v-if="panelExpanded" :style="panelStyle">
        <!-- Refactor Approach -->
        <v-card-title>MathDeck Search</v-card-title>
        
        <math-search-box></math-search-box>
        <equation-viewer></equation-viewer>
        <chip-display></chip-display>

         <v-btn 
        :style="panelStyle"
        tile
        color="#f46d04"
        class="white--text  ma-0 pa-0"
        @click="toggleCollapse"
        >
            Close
        </v-btn>

        <!-- iframe -->
        <!-- <iframe src="https://mathdeck.org/#l0TqDpfh9uklOn1SPCibxIq6u8VRotSmyY2vQd2K0_Xh" width="900px" height="600px"></iframe> -->

        <!-- Client-side only --> 
        <!-- <client-only placeholder="Loading...">
            <chip></chip>
        </client-only> -->

    </v-card>
    


    <v-btn 
        v-else 
        :style="panelStyle"
        tile
        color="#f46d04"
        class="white--text"
        @click="toggleCollapse"
    >
         MathDeck
    </v-btn>

</template>


<script>
import MathSearchBox from './MathSearchBox.vue';
import EquationViewer from './EquationViewer.vue';
import ChipDisplay from './ChipDisplay.vue';
// import Chip from './Chip.vue';

export default {
    components: {
        MathSearchBox,
        EquationViewer,
        ChipDisplay,
        // Chip
    },
    data() {
        return {
            panelExpanded: false,
        }
    },
    computed: {
        panelStyle() {
            return (this.panelExpanded) ? 
            {
                width: '700px',
                minWidth: '300px',
                borderRadius: '0',
                margin: '100px 0 0 0',
                position: 'absolute',
                right: '0',
                zIndex: '100'
            } : {
                width: '150px',
                minWidth: '100px',
                borderRadius: '0',
                float: 'right',
                margin: '100px 0 0 0',
                position: 'absolute',
                right: '0',
            };
        }
    },
    methods: {
        toggleCollapse() {
            this.panelExpanded = !this.panelExpanded;
        }
    }
}
</script>