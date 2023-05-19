<template>
    <div>
        <error-message :is-fetch-error="isFetchError" :message="message"/>
        <b-button-group>
            <b-button variant="primary" class="mb-2" v-b-modal.columns-config-modal>
                Show Columns Picker
            </b-button>
        </b-button-group>

        <BTableColumnsPicker
                :allColumns="allColumns"
                :currentColumns="columns"
                :id="'columns-config-modal'"
                @apply="applyColumnConfigs"
        />
        <b-spinner small v-if="loading"></b-spinner>
        <b-form-group id="input-group-3" label="Instrument" label-for="instr" v-if="'Prices' == table">
            <b-form-select multiple :options="instrs" id="instr" v-model="selectedInstrs"></b-form-select>
        </b-form-group>

        <fx-tab :columns="columns" :auth="auth" :datas="datas" :all_columns="allColumns"
                :table="table" v-if="!IsPricesTable"/>
        <fx-tab v-else :instr="instr" :auth="auth" :columns="columns" :datas="datas" :all_columns="allColumns"
                :table="table" v-for="instr in selectedInstrs" />

    </div>
</template>
<script lang="ts">
import {Component, Prop, Vue, Watch} from "vue-property-decorator";
import {AuthCredentials} from "@/views/AuthCredentials";
import ErrorMessage from "@/views/ErrorMessage.vue";
import BTableColumnsPicker from "@/components/BTableColumnsPicker.vue";
import FxTab from "@/views/FxTab.vue";


@Component({
    components: {FxTab, BTableColumnsPicker, ErrorMessage}
})
export default class TablePrinter extends Vue {
    allColumns: string[] = [];
    loading = false;
    instr: string = "USD/CAD"
    instrs: string[] = ["USD/CAD", "USD/JPY", "USD/CHF", "XAU/USD", "GPB/USD"]
    selectedInstrs: string[] = ["USD/CAD", "USD/JPY", "USD/CHF", "XAU/USD", "GPB/USD"]

    get IsPricesTable() {
        return this.table === "Prices"
    }

    applyColumnConfigs(new_columns: string[]) {
        this.columns = new_columns;
        localStorage.setItem(this.table, JSON.stringify(this.columns))
    }


    columns: string[] = [];
    datas: {}[] = []
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

.negative {
    color: #dc3545 !important;
}
</style>