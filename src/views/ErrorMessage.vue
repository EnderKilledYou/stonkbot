<template>
    <b-alert show variant="danger" v-if="isFetchError">{{ message }}</b-alert>
</template>
<script lang="ts">
export default {
    name: 'error-message',
    props: {
        isFetchError: {},
        message: {}
    }
}
</script>