<template>
    <b-container fluid id="app">

          <table-viewer/>
    </b-container>
</template>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #d7ac08;
        background-color: #295fa6 !important;
    min-height: 100vh;
}


nav {
    padding: 30px;
}

nav a {
    font-weight: bold;
    color: #2c3e50;
}

nav a.router-link-exact-active {
    color: #42b983;
}
</style>
<script setup lang="ts">
import TableViewer from "@/views/TableViewer.vue";
</script>