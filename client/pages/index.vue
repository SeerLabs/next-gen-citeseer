<template>
    <div id="homepage">
        <img id="logo" src="../assets/img/csx_logo.png" alt="CiteSeerX" />
        <search-box/>
    </div>
</template>

<script>
import SearchBox from '~/components/SearchBox.vue';

export default {
    components: {
        SearchBox
    },
};
</script>

<style>
#homepage {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin: 10% auto;
    width: 75vw;
}

#logo {
    width: 20em;
    margin-bottom: 1em;
}
</style>
