<template>
    <div>
        <b-button-group>
            <b-button variant="primary" class="mb-2" @click="load_table">
                Load
            </b-button>
            <b-button variant="success" class="mb-2" @click="autoRefresh" v-if="!interval">
                Auto Refresh
            </b-button>
            <b-button variant="danger" class="mb-2" @click="autoRefreshOff" v-if="interval">
                Stop Auto Refresh
            </b-button>
            <b-button variant="primary" class="mb-2" v-b-modal="'columns-config-modal' + instr">
                Show Columns Picker
            </b-button>
            <b-button v-if="loading">
                <b-spinner small></b-spinner>
            </b-button>
        </b-button-group>

        <BTableColumnsPicker
                :allColumns="all_columns"
                :currentColumns="columns"
                :id="'columns-config-modal' + instr"
                @apply="applyColumnConfigs"
        />
        <b-card v-if="table === 'Offers' && datas.length >0">

            <b-form-group
                    label="Amount"
                    label-for="amount_to_buy">
                <b-input type="number" min="0" id="amount_to_buy" v-model="amount_to_buy"></b-input>
            </b-form-group>
            <b-form-group
                    label="Instrument"
                    label-for="select_instrument">
                <b-form-select :options="all_instrs" id="select_instrument"
                               v-model="selected_instr"></b-form-select>
            </b-form-group>
            <b-button variant="success" v-if="selected_instr.length >0" @click="Buy_Instrument">Buy
                {{ selected_instr }}
            </b-button>

        </b-card>
        <forex-table :columns="columns"   :datas="datas"
                       :instr="instr" :table="table"/>
    </div>
</template>
<script lang="ts">


import {Component, Prop, Vue} from "vue-property-decorator";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";
import ErrorMessage from "@/views/ErrorMessage.vue";
import {AuthCredentials} from "@/views/AuthCredentials";
import ForexTable from "@/components/ForexTable.vue";

const api = require('../api.js')




@Component({
    components: {ForexTable,  BTableColumnsPicker, ErrorMessage}
})

export default class FxTab extends Vue {
    columns: string [] = [];
    datas: { [key: string]: any }[] = []
    @Prop({default: ''}) table!: string;
    @Prop() instr!: string;
    @Prop() auth!: AuthCredentials;
    all_columns: string[] = []
    amount_to_buy: number = 0;
    selected_instr: string = ''
    private loading: boolean = false
    private interval: number | null = 0


    get all_instrs() {
        return this.datas.map(a => a['instrument'])
    }

    async Buy_Instrument() {
        alert("???")
     //   const result = await api.API.buy_order(this.selected_instr, this.amount_to_buy, this.rate, this.auth.userHash)
    }

    beforeUnmount() {
        if (this.interval) {
            clearInterval(this.interval);

        }
    }



    applyColumnConfigs(new_columns: string[]) {
        this.columns = new_columns;
        localStorage.setItem(this.table, JSON.stringify(this.columns))
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
        if (this.loading) {
            return;
        }
        try {

            this.loading = true;
            let result;
            switch (this.table) {
                case "Prices":
                    if (this.instr.length > 0) {
                        result = await api.API.get_price_history(this.instr, this.auth.userHash)
                        this.process_result(result);
                    }
                    break;
                case "Summary":

                    result = await api.API.get_summary_trades_table_api( this.auth.userHash)
                    this.process_result(result);

                    break;
                case "Orders":
                    result = await api.API.get_orders_table_api(this.auth.userHash)

                    this.process_result(result);
                    break;
                case "Trades":
                    result = await api.API.get_trades_table_api( this.auth.userHash)
                    this.process_result(result);
                    break;
                case "Messages":
                    result = await api.API.get_messages_trades_table_api( this.auth.userHash)
                    this.process_result(result);
                    break;
                case "Closed Trades":
                    result = await api.API.get_closed_trades_table_api( this.auth.userHash)
                    this.process_result(result);
                    break;
                case "Offers":
                    result = await api.API.get_offers_table_api( this.auth.userHash)
                    this.process_result(result);
                    break;
                case "Accounts":
                    result = await api.API.get_accounts_table_api( this.auth.userHash)
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
            this.all_columns = this.columns
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