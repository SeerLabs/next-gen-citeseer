<template>
    <v-menu bottom offset-y>
        <template v-slot:activator="{ on }">
            <v-chip 
            v-on="on"
            :draggable="true"
            @dragstart="startDrag($event)"
            @dragover.stop
            >
            2x + 3
            </v-chip>
        </template>
        <v-btn @click="postMessage">
            Add to MathDeck
        </v-btn>
    </v-menu>
   
</template>

<script>
export default {
    data() {
        return {
            equation: '3x - y',
        }
    },
    methods: {
        postMessage() {
            const iframe = window.frames.dummyIframe
            const json = {type: 'chip', string: '2x+3'}
            iframe.postMessage(JSON.stringify(json), 'http://localhost:8080/')
        },
        startDrag(event) {
            const data = {
                type: 'chip',
                string: '2x+3'
            }
            event.dataTransfer.setData('text/plain', JSON.stringify(data))
        },
    },
}
</script>