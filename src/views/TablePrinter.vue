<template>
    <div>
        <error-message :is-fetch-error="isFetchError" :message="message"/>
        <b-button-group>
            <b-button variant="primary" class="mb-2" v-b-modal.columns-config-modal>
                Show Columns Picker
            </b-button>
        </b-button-group>
        <b-button variant="success" class="mb-2" @click="autoRefresh" v-if="!interval && 'Prices' == table">
            Auto Refresh
        </b-button>
        <b-button variant="danger" class="mb-2" @click="autoRefreshOff" v-if="interval && 'Prices' == table" >
            Stop Auto Refresh
        </b-button>
        <BTableColumnsPicker
                :allColumns="allColumns"
                :currentColumns="columns"
                :id="'columns-config-modal'"
                @apply="applyColumnConfigs"
        />
        <b-spinner small v-if="loading"></b-spinner>
        <b-form-group id="input-group-3" label="Instrument" label-for="instr" v-if="'Prices' == table">
            <b-form-input type="text" id="instr" v-model="instr"></b-form-input>
        </b-form-group>
        <b-button variant="success" class="mb-2" @click="load_table" v-if="'Prices' == table">
            Load
        </b-button>
        <b-table-simple striped hover caption-top responsive class="">
            <caption>{{ table }} Table</caption>
            <b-thead head-variant="dark">
                <b-tr>
                    <b-th v-for="column in columns">
                        {{ correctSpace(column) }}
                    </b-th>
                </b-tr>
            </b-thead>
            <b-tbody>
                <b-tr v-for="data in datas">
                    <b-td v-for="column in columns" :class="getCellClasses(column,data[column])">

                        {{ data[column] }}
                    </b-td>
                </b-tr>
            </b-tbody>
        </b-table-simple>
    </div>
</template>
<script lang="ts">
import {Component, Prop, Vue, Watch} from "vue-property-decorator";
import {AuthCredentials} from "@/views/AuthCredentials";
import ErrorMessage from "@/views/ErrorMessage.vue";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";

const space = require('to-space-case');
const api = require('../api.js')

function isNumber(rowValue: any) {
    return !isNaN(+rowValue);
}

@Component({
    components: {BTableColumnsPicker, ErrorMessage}
})
export default class TablePrinter extends Vue {
    allColumns: string[] = [];
    loading = false;
    interval: number | null = 0
    instr: string = "EUR/USD";

    applyColumnConfigs(new_columns: string[]) {
        this.columns = new_columns;
        localStorage.setItem(this.table, JSON.stringify(this.columns))
    }


    correctSpace(st: string) {
        return space(st)
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

    columns: string[] = [];
    datas: {}[] = []
    message: string = '';
    isFetchError: boolean = false;
    @Prop() table!: string;
    @Prop() auth!: AuthCredentials;

    @Watch('table')
    async tableSelectionChange(new_val: string, old_val: string) {
        await this.load_table();

    }

    autoRefresh() {
        if (!this.interval) {
            this.interval = setInterval(this.load_table.bind(this), 10000)
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
            this.isFetchError = true;
            this.message = e.message;

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

        this.allColumns = this.columns
        this.datas = result.tbl;
        this.isFetchError = false;
        this.message = '';
    }

    async created() {
        debugger;
        switch (this.table) {
            case "Summary":

                try {
                    const result = await api.API.get_summary_trades_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.columns = result.columns;
                    this.datas = result.data;
                    this.isFetchError = false;
                    this.message = '';
                } catch (e: any) {
                    console.log(e);
                    this.isFetchError = true;
                    this.message = e.message;
                }
                break;

        }
    }

    private print_error(e: any) {
        this.isFetchError = true;
        this.message = e.error;
    }
}
</script>

<style>
.positive {
    color: #198754 !important;
}

.neutral {
    color: #2a95bf !important;
}

.background {
    color: #595959 !important;
}

.negative {
    color: #dc3545 !important;
}
</style>