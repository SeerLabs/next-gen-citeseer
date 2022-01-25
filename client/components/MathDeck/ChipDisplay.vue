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
            equations: ['equation1', 'equation2', 'equation3', 'equation4', 'equation5']
        }
    }
}
</script>