<template>
    <v-container>
        <v-chip-group>
            <v-chip 
            v-for="equation in equations" 
            :key="equation">
            {{ equation }}
            </v-chip>
        </v-chip-group>
    </v-container>
</template>

<script>
export default {
    data() {
        return {
            equations: ['cos x', 'sin x', 'arcsin x', 'tan x']
        }
    }
}
</script>