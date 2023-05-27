<template>
    <div>
        <b-alert variant="success" show v-if="success">
            {{ last_success }}
        </b-alert>
        <b-alert show variant="danger" v-if="isFetchError">{{ message }}</b-alert>
        <b-spinner v-if="loading"></b-spinner>
        <fx-tab :instr="instr" :auth="auth"
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

const api = require('../api.js')
const space = require('to-space-case');


@Component({
    components: {PricesTabInstance, FxTab, BTableColumnsPicker, ErrorMessage}
})

export default class TradesTab extends Vue {
    @Prop({default: ''}) table!: string;
    @Prop() instr!: string;
    @Prop() auth!: AuthCredentials;
    button_columns = [{'column': 'trade_id', 'column_text': 'Close '}]
    loading: boolean = false;
    last_success: string = ''
    message: string = ''
    success: boolean = false

    isFetchError: boolean = false;

    cell_click(column: string, value: string, row: any) {
        switch (column) {
            case "instrument":
                alert(value)
                break;
        }

    }

    private print_error(e: any) {
        this.isFetchError = true;
        this.message = e.message;


    }


}
</script>