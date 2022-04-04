<template>

    <v-card v-if="panelExpanded" :style="panelStyle">
        <!-- Refactor Approach -->
        <!-- <v-card-title>MathDeck Search</v-card-title>
        
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
        </v-btn> -->

        <!-- iframe -->
        <chip></chip>

        <div class="drop-box mt-5" @drop.prevent="onDrop($event)" @dragenter="checkDrop" @dragover="checkDrop">
        <iframe name="dummyIframe" src="http://localhost:8080/" width="900px" height="700px">
        </iframe>
        </div>

        <!-- <iframe name="dummyIframe" src="https://www.mathdeck.org/#uZN2a57wosmbxPVKryMk6YP3mHYCKwBbQ5-GfEAjaGeR" width="900px" height="600px"></iframe> -->

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
// import MathSearchBox from './MathSearchBox.vue';
// import EquationViewer from './EquationViewer.vue';
// import ChipDisplay from './ChipDisplay.vue';
import Chip from './Chip.vue';

export default {
    components: {
        // MathSearchBox,
        // EquationViewer,
        // ChipDisplay,
        Chip
    },
    data() {
        return {
            panelExpanded: false,
            msg: '',
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
    mounted() {
        window.addEventListener('message', this.receiveMsg, false)
    },
    methods: {
        toggleCollapse() {
            this.panelExpanded = !this.panelExpanded;
        },
        
        postMessage() {
            const iframe = window.frames.dummyIframe
            const json = {type: 'chip', string: '2x+3'}
            iframe.postMessage(JSON.stringify(json), 'http://localhost:8080/')
        },

        receiveMsg(event) {
            if (event.origin === "http://localhost:8080") {
                this.msg = event.data
            } else {
                this.msg = ''
            }
      },
      checkDrop(event) {
          event.preventDefault()
      },
      onDrop(event) {
          const data = JSON.parse(event.dataTransfer.getData('text/plain'))

          const iframe = window.frames.dummyIframe
          iframe.postMessage(JSON.stringify(data), 'http://localhost:8080/')

          console.log(data)
      },
    }
}
</script>

<style>
    .drop-box {
        border: dashed 3px red;
        height: 750px;
        width: 900px;
    }
</style>