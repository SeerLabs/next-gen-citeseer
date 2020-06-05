
<template>
    <object id="fit-screen" v-bind:data="pdfURL" type="application/pdf">
        <embed v-bind:src="pdfURL" type="application/pdf" />
    </object>

</template>

<script>

export default {
    data(){
        return{
            pdfURL: "http://localhost:8000/api/document?repid=rep1&type=pdf&doi="
        }
    },
    mounted(){
        this.pdfURL += this.$route.params.id
    }
}
</script>

<style>
#fit-screen {
   margin: 0px;
   height: 100vh;
   width: 100%;
}
</style>
