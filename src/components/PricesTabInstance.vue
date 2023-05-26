<template>
    <div>
        <b-form-group
                label="Amount"
                label-for="amount_to_buy">
            <b-input type="number" class="text-right" step=".01" min="0" id="amount_to_buy"
                     v-model="amount"></b-input>
        </b-form-group>
        <b-button-group>
            <b-button variant="success" @click="buy_market">Buy Market</b-button>
            <b-button variant="danger" @click="sell_market">Sell Market</b-button>
        </b-button-group>
        <b-alert variant="success" show v-if="success">
            {{ last_success }}
        </b-alert>
        <b-alert show variant="danger" v-if="isFetchError">{{ message }}</b-alert>
        <fx-tab :instr="instr" :auth="auth"
                :table="table" @fetch_error="print_error"/>
    </div>
</template>
<script lang="ts">
import FxTab from "@/components/FxTab.vue"
import {Component, Prop, Vue} from "vue-property-decorator";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";
import ErrorMessage from "@/views/ErrorMessage.vue";
import {AuthCredentials} from "@/views/AuthCredentials";

const api = require('../api.js')
const space = require('to-space-case');
@Component({
    components: {FxTab, BTableColumnsPicker, ErrorMessage}
})

export default class PricesTab extends Vue {
    amount: number = 0
    @Prop() table!: string;
    @Prop() instr!: string;
    loading: boolean = false;
    last_success: string = ''
    success: boolean = false
    @Prop() auth!: AuthCredentials;
    isFetchError: boolean = false;
    message: string = '';

    private async buy_market( ) {

        try {
            this.clear_error();
            this.loading = true;
            const result = await api.API.buy_market(this.instr, +this.amount, this.auth.userHash)
            if (result) {
                if (result.success) {

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
 private async sell_market() {

        try {
            this.clear_error();
            this.loading = true;
            const result = await api.API.sell_market(this.instr, +this.amount, this.auth.userHash)
            if (result) {
                if (result.success) {

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

    private print_success(success: string) {
        this.last_success = success
        this.success = true;

    }

    private clear_error() {
        this.success = false;
        this.last_success = '';
        this.isFetchError = false;
        this.message = '';


    }

    private print_error(e: any) {
        this.isFetchError = true;
        this.message = e.message;


    }
}
</script>