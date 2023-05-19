<template>
    <div>
        <b-button-group>
            <b-button variant="primary" class="mb-2" @click="load_table" v-if="'Prices' == table">
                Load
            </b-button>
            <b-button variant="success" class="mb-2" @click="autoRefresh" v-if="!interval && 'Prices' == table">
                Auto Refresh
            </b-button>
            <b-button variant="danger" class="mb-2" @click="autoRefreshOff" v-if="interval && 'Prices' == table">
                Stop Auto Refresh
            </b-button>
            <b-button v-if="loading">
                <b-spinner small ></b-spinner>
            </b-button>
        </b-button-group>
        <b-table-simple striped hover caption-top responsive class="">
            <caption>{{ instr }} {{ table }} Table</caption>
            <b-thead head-variant="dark">
                <b-tr>
                    <b-th v-for="column in columns">
                        {{ correctSpace(column) }}
                    </b-th>
                </b-tr>
            </b-thead>
            <b-tbody>
                <b-tr v-for="data in datas">
                    <b-td v-for="column in columns" :class="getCellClasses">

                        {{ data[column] }}
                    </b-td>
                </b-tr>
            </b-tbody>
        </b-table-simple>
    </div>
</template>
<script lang="ts">
import {Component, Prop, Vue} from "vue-property-decorator";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";
import ErrorMessage from "@/views/ErrorMessage.vue";
import {AuthCredentials} from "@/views/AuthCredentials";

const api = require('../api.js')
const space = require('to-space-case');

function isNumber(rowValue: any) {
    return !isNaN(+rowValue);
}

@Component({
    components: {FxTab, BTableColumnsPicker, ErrorMessage}
})

export default class FxTab extends Vue {
    @Prop({default: []}) columns!: string [];
    @Prop({default: []}) datas!: {}[]
    @Prop({default: ''}) table!: string;
    @Prop() instr!: string;
    @Prop() auth!: AuthCredentials;
    @Prop({default: []}) all_columns!: string[]
    private loading: boolean = false
    private interval: number | null = 0

    correctSpace(st: string) {
        return space(st)
    }

    beforeUnmount() {
        if (this.interval) {
            clearInterval(this.interval);

        }
    }

    getCellClasses(columnName: string, rowValue: any) {
        if (!isNumber(rowValue)) {
            return ["background"];
        }
        if (rowValue === 0) {
            return ["neutral"]
        }
        if (rowValue < 0) {
            return ["negative"];
        } else if (rowValue > 0) {
            return ["positive"]
        }

    }

    autoRefresh() {
        if (!this.interval) {
            this.interval = setInterval(this.load_table.bind(this), 1000)
        }
    }

    autoRefreshOff() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;

        }
    }

    private async load_table() {
        try {
            debugger;
            this.loading = true;
            let result;
            switch (this.table) {
                case "Prices":
                    if (this.instr.length > 0) {
                        result = await api.API.get_price_history(this.instr, this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                        this.process_result(result);
                    }
                    break;
                case "Summary":

                    result = await api.API.get_summary_trades_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.process_result(result);

                    break;
                case "Orders":
                    result = await api.API.get_orders_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)

                    this.process_result(result);
                    break;
                case "Trades":
                    result = await api.API.get_trades_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.process_result(result);
                    break;
                case "Messages":
                    result = await api.API.get_messages_trades_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.process_result(result);
                    break;
                case "Closed Trades":
                    result = await api.API.get_closed_trades_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.process_result(result);
                    break;
                case "Offers":
                    result = await api.API.get_offers_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.process_result(result);
                    break;
                case "Accounts":
                    result = await api.API.get_accounts_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.process_result(result);
                    break;
                default:

                    return;
            }
        } catch (e: any) {
            this.print_error(e)


        } finally {
            this.loading = false;
        }
    }

    private process_result(result: any) {
        if (!result) {
            return;
        }
        if (result.error) {
            this.print_error(result);
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
            }
            return;
        }
        this.update_table(result);
    }

    private update_table(result: any) {
        const existing_columns_setup = localStorage.getItem(this.table);
        if (existing_columns_setup) {
            this.columns = JSON.parse(existing_columns_setup);
        } else {
            this.columns = result.columns;
            localStorage.setItem(this.table, JSON.stringify(this.columns))
        }

        this.all_columns = this.columns
        this.datas = result.tbl;
        this.$emit('fetch_success')
    }


    private print_error(e: any) {
        this.$emit("fetch_error", e)
    }
}
</script>