<template>
    <table-viewer/>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';

import TableViewer from "@/views/TableViewer.vue"; // @ is an alias to /src

@Component({
  components: {
      TableViewer,
  },
})
export default class HomeView extends Vue {}
</script>
