<template>
    <div>
        <b-alert variant="success" show v-if="success">
            {{ last_success }}
        </b-alert>
        <b-alert show variant="danger" v-if="isFetchError">{{ message }}</b-alert>
        <b-spinner v-if="loading"></b-spinner>
        <fx-tab :instr="instr" :auth="auth" :column_key="column_key"
                @cell_click="cell_click" :table="table" @fetch_error="print_error" :button_columns="button_columns"/>

    </div>
</template>
<script lang="ts">
import FxTab from "@/components/FxTab.vue"
import {Component, Prop, Vue} from "vue-property-decorator";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";
import ErrorMessage from "@/views/ErrorMessage.vue";
import {AuthCredentials} from "@/views/AuthCredentials";
import PricesTabInstance from "@/components/PricesTabInstance.vue";
import {column_property} from "@/components/Column_property";

const api = require('../api.js')


@Component({
    components: {PricesTabInstance, FxTab, BTableColumnsPicker, ErrorMessage}
})

export default class TradesTab extends Vue {
    @Prop({default: ''}) table!: string;
    @Prop() instr!: string;
    @Prop() auth!: AuthCredentials;
    column_key = 'trade_id'
    button_columns: column_property[] = [{'column': 'trade_id', 'column_text': 'Market Close '}]
    loading: boolean = false;
    last_success: string = ''
    message: string = ''
    success: boolean = false

    isFetchError: boolean = false;

    cell_click(column: string, value: string, row: any) {
        console.log(column)
        switch (column) {
            case "trade_id":

                this.close_trade(row);
                break;
        }

    }

    async close_trade(row: any) {
        try {
            this.clear_error();
            this.loading = true;
            const result = await api.API.close_trade(row['instrument'], +row['amount'], +row['trade_id'], this.auth.userHash)
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

    private clear_error() {
        this.success = false;
        this.last_success = '';
        this.$emit("fetch_error", null)

    }

    private print_success(success: string) {
        alert(success);

    }

    private print_error(e: any) {
        this.isFetchError = true;
        this.message = e.message;


    }


}
</script>