<template>
    <div>
        <error-message :is-fetch-error="isFetchError" :message="message"/>
        <b-spinner v-if="loading"></b-spinner>
        <h2 v-if="isAuthed">{{ authCredentials.username }}</h2>
        <login-form :auth.sync="authCredentials" v-show="!isAuthed" @login="LoginAttempt"/>
        <table-selector :table.sync="table" :tables="tables" v-show="isAuthed"/>
        <table-printer :auth="authCredentials" :table="table" v-show="IsTableSelected"/>

    </div>
</template>
<script lang="ts">
import {Component, Vue, Watch} from 'vue-property-decorator';
import LoginForm from "@/views/LoginForm.vue";
import {AuthCredentials} from "@/views/AuthCredentials";
import TableSelector from "@/views/TableSelector.vue";
import TablePrinter from "@/components/TablePrinter.vue";
import ErrorMessage from "@/views/ErrorMessage.vue";

const api = require('@/api.js')

@Component({
    components: {ErrorMessage, TablePrinter, TableSelector, LoginForm},
})
export default class TableViewer extends Vue {
    isAuthed: boolean = false;
    private isFetchError: boolean = false;
    private message: string = '';
    private loading: boolean = false;

    get IsTableSelected(): boolean {
        return this.table !== "Pick One";

    }

    authCredentials: AuthCredentials = {
        username: 'D25946643',
        password: '0dWql',
        url: 'https://www.fxcorporate.com/Hosts.jsp',
        connectionType: 'Demo'
    }
    table = 'Pick One'
    tables = [
        "Pick One",
        'Orders',
        'Prices',
        'Offers',
        'Accounts',
        'Closed Trades',
        'Messages',
        'Summary',
        'Trades'
    ]


    @Watch('table') onTableSelectionChange(new_val: string, old_val: string) {

    }


    async LoginAttempt() {
        this.loading = true;
        try {
            const loginResult = await api.API.login(this.authCredentials.username, this.authCredentials.password, this.authCredentials.url, this.authCredentials.connectionType, '', '')
            if (loginResult.authenticated) {
                this.isAuthed = true;
                this.authCredentials.userHash = loginResult.user_hash
                this.isFetchError = false;
                this.message = '';
            }

        } catch (e: any) {
            this.isFetchError = true;
            this.message = e.message;
        } finally {
            this.loading = false;
        }

    }

    async created() {

    }
}
</script>