<template>
    <div>
        <error-message :is-fetch-error="isFetchError" :message="message"/>

        <b-spinner small v-if="loading"></b-spinner>
        <b-form-group id="input-group-3" label="Instrument" label-for="instr" v-if="'Prices' == table">
            <b-form-select multiple :options="instrs" id="instr" v-model="selectedInstrs"></b-form-select>
        </b-form-group>
        <offers-tab :auth="auth" v-if="IsOffersTable" @fetch_error="print_error"/>
        <fx-tab :auth="auth"
                :table="table" v-else-if="!IsPricesTable" @fetch_error="print_error"/>
        <prices-tab v-else :auth="auth" @fetch_error="print_error" :selected-instrs="selectedInstrs"
                    :table="table"/>

    </div>
</template>
<script lang="ts">
import {Component, Prop, Vue, Watch} from "vue-property-decorator";
import {AuthCredentials} from "@/views/AuthCredentials";
import ErrorMessage from "@/views/ErrorMessage.vue";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";
import FxTab from "@/components/FxTab.vue";
import OffersTab from "@/components/OffersTab.vue";
import PricesTab from "@/components/PricesTab.vue";


@Component({
    components: {PricesTab, OffersTab, FxTab, BTableColumnsPicker, ErrorMessage}
})
export default class TablePrinter extends Vue {

    loading = false;
    instr: string = "USD/CAD"
    instrs: string[] = ["USD/CAD", "USD/JPY", "USD/CHF", "XAU/USD", "GPB/USD"]
    selectedInstrs: string[] = ["USD/CAD", "USD/JPY", "USD/CHF", "XAU/USD", "GPB/USD"]

    get IsOffersTable() {
        return this.table === "Offers"
    }

    get IsPricesTable() {
        return this.table === "Prices"
    }

    print_error(e: any) {

        if (e) {
            this.isFetchError = true;
            this.message = e.message;
            return;
        }
        this.isFetchError = false;
        this.message = '';
    }

    message: string = '';
    isFetchError: boolean = false;
    @Prop() table!: string;
    @Prop() auth!: AuthCredentials;

    @Watch('table')
    async tableSelectionChange(new_val: string, old_val: string) {
        //  await this.load_table();

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

.white {
    color: #08210c !important;
}

.negative {
    color: #dc3545 !important;
}
</style>