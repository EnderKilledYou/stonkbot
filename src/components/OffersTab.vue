<template>
    <div>
        <b-button-group class="mx-1">
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
            <BTableColumnsPicker
                    :allColumns="all_columns"
                    :currentColumns="columns"
                    :id="'columns-config-modal' "
                    @apply="applyColumnConfigs"
            />
        </b-button-group>


        <b-input-group size="sm" class="justify-content-between">
            <b-form-group
                    label="Filter"
                    label-for="select_instrument">
                <b-form-select multiple :options="all_instrs" id="filter_instrument"
                               v-model="selected_instrs"></b-form-select>
            </b-form-group>

            <b-form-group
                    label="Rate"
                    label-for="rate">
                <b-input type="number" class="text-right" step=".01" min="0" id="rate" v-model="rate"></b-input>
            </b-form-group>
            <b-form-group
                    label="Amount"
                    label-for="amount_to_buy">
                <b-input type="number" class="text-right" step=".01" min="0" id="amount_to_buy"
                         v-model="amount_to_buy"></b-input>
            </b-form-group>

            <b-form-group
                    label="Instrument"
                    label-for="select_instrument">
                <b-form-select :options="all_instrs" id="select_instrument"
                               v-model="selected_instr"></b-form-select>
            </b-form-group>

            <b-form-group
                    label="Order Type"
                    label-for="select_type">
                <b-form-select :options="all_order_type" v-model="order_type">

                </b-form-select>
            </b-form-group>
        </b-input-group>
        <b-button variant="success" v-if="can_show_buy_button"
                  @click="Buy_Instrument">Buy
            {{ amount_to_buy }} of {{ rate }}
            {{ selected_instr }}
        </b-button>
        <b-button variant="danger" v-if="can_show_sell_button"
                  @click="Sell_Instrument">Sell
            {{ amount_to_buy }} of {{ rate }}
            {{ selected_instr }}
        </b-button>
        <b-alert variant="success" show v-if="success">
            {{ last_success }}
        </b-alert>
        <forex-table :columns="columns" :datas="filtered_datas" @cell_click="cell_click"
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
const space = require('to-space-case');


@Component({
    components: {ForexTable, BTableColumnsPicker, ErrorMessage}
})

export default class OffersTab extends Vue {
    columns: string [] = [];
    datas: { [key: string]: any }[] = []
    @Prop({default: ''}) table!: string;
    @Prop() instr!: string;
    @Prop() auth!: AuthCredentials;
    all_columns: string[] = []
    order_type: string = "ENTRY"
    all_order_type: string[] = ["LIMIT",
        "LIMIT_ENTRY",
        "ENTRY",
        "CLOSE_ENTRY",
        "STOP_ENTRY",
        "MARKET_CLOSE",
        "MARKET_CLOSE_RANGE",
        "MARKET_OPEN",
        "MARKET_OPEN_RANGE",
        "OPEN_LIMIT",
        "STOP",
        "STOP_ENTRY",
        "TRUE_MARKET_CLOSE",
        "TRUE_MARKET_OPEN"]
    amount_to_buy: number = 0;
    selected_instr: string = ''
    rate: number = 0.0
    private loading: boolean = false
    private interval: number | null = 0
    last_success: string = '';
    success = false

    get filtered_datas() {
        return this.datas.filter(this.filter_instrs)


    }

    get can_show_sell_button() {
        return this.selected_instr.length > 0 && this.amount_to_buy > 0 && this.rate > 0
    }

    get can_show_buy_button() {
        return this.selected_instr.length > 0 && this.amount_to_buy > 0 && this.rate > 0
    }

    cell_click(column: string, value: string, row: any) {
        switch (column) {
            case "instrument":
                this.selected_instr = value;
                this.rate = +row['ask']
                break;
        }

    }

    filter_instrs(a: any) {

        return this.selected_instrs.includes(a['instrument']);
    }

    selected_instrs: string[] = ["USD/CAD", "USD/JPY", "USD/CHF", "XAU/USD", "GPB/USD"]

    get all_instrs() {
        return this.datas.map(a => a['instrument'])
    }

    async Sell_Instrument() {
        try {
            this.clear_error();
            this.loading = true;
            const result = await api.API.sell_order(this.selected_instr, +this.amount_to_buy, +this.rate, this.order_type, this.auth.userHash)
            if (result) {
                if (result.success) {
                    debugger;
                    this.print_success(result.message)
                } else if (result.message) {
                    this.print_error({message: result.message})
                }

            } else {
                this.print_error({message: "Nothing was returned"})
            }
        } catch (e: any) {
            this.print_error({message: e.message})


        } finally {
            this.loading = false;
        }
    }

    async Buy_Instrument() {
        try {
            this.clear_error();
            this.loading = true;
            const result = await api.API.buy_order(this.selected_instr, +this.amount_to_buy, +this.rate, this.order_type,  this.auth.userHash)
            if (result) {
                if (result.success) {
                    debugger;
                    this.print_success(result.message)
                } else if (result.message) {
                    this.print_error({message: result.message})
                }

            } else {
                this.print_error({message: "Nothing was returned"})
            }
        } catch (e: any) {
            this.print_error({message: e.message})


        } finally {
            this.loading = false;
        }
    }

    beforeDestroy() {
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

            result = await api.API.get_offers_table_api( this.auth.userHash)
            this.process_result(result);


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
            this.print_error({message: result.error});
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
            }
            return;
        }
        this.update_table(result);
        this.clear_error();
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

    private clear_error() {
        this.success = false;
        this.last_success = '';
        this.$emit("fetch_error", null)

    }

    private print_error(e: any) {
        this.$emit("fetch_error", e)
        console.log(e);
    }

    private print_success(success: string) {
        this.last_success = success
        this.success = true;

    }
}
</script>