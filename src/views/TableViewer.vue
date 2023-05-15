<template>
    <div>
        <login-form :auth.sync="authCredentials"/>

    </div>
</template>
<script lang="ts">
import {Component, Vue, Watch} from 'vue-property-decorator';
import LoginForm from "@/views/LoginForm.vue";
import {AuthCredentials} from "@/views/AuthCredentials";


@Component({
    components: {LoginForm},
})
export default class TableViewer extends Vue {
    authCredentials: AuthCredentials = {
        username: '',
        password: ''
    }

    @Watch('authCredentials.username', {deep: true})
    onAuthValueChanged(val: AuthCredentials) {
        console.log(val)
    }

    async created() {

    }
}
</script>