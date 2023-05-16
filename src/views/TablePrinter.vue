<template>
    <div>
        <error-message :is-fetch-error="isFetchError" :message="message"/>
        <b-table-simple hover   caption-top responsive class="background">
            <caption>{{ table }} Table</caption>
            <b-thead head-variant="dark">
                <b-tr>
                    <b-th v-for="column in columns">
                        {{ column }}
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

const api = require('../api.js')

function isNumber(rowValue: any) {
    return !isNaN(+rowValue);
}

@Component({
    components: {ErrorMessage}
})
export default class TablePrinter extends Vue {


    getCellClasses(columnName: string, rowValue: any) {
        if (!isNumber(rowValue)) {
            return ["background"];
        }
        if (rowValue === 0) {
            return ["neutral"]
        }
        if (rowValue < 0) {
            return ["negative"];
        }
        return ["positive"]
    }

    columns: string[] = [];
    datas: {}[] = []
    message: string = '';
    isFetchError: boolean = false;
    @Prop() table!: string;
    @Prop() auth!: AuthCredentials;

    @Watch('table')
    async tableSelectionChange(new_val: string, old_val: string) {
        debugger;
        switch (this.table) {
            case "Summary":

                try {
                    const result = await api.API.get_summary_trades_table_api(this.auth.username, this.auth.password, this.auth.url, this.auth.connectionType)
                    this.columns = result.result.columns;
                    this.datas = result.result.tbl;
                    this.isFetchError = false;
                    this.message = '';
                } catch (e: any) {
                    this.isFetchError = true;
                    this.message = e.message;
                }
                break;

        }
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
}
</script>

<style>
.positive {
    background-color: #295fa6;
}

.neutral {
    background-color: #2a95bf;
}

.background {
    background-color: #595959;
}

.negative {
    background-color: #bf0413;
}
</style>