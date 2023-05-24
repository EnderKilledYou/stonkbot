<template>
    <b-table-simple striped hover caption-top responsive class="">
        <caption>{{ instr }} {{ table }} Table</caption>
        <b-thead head-variant="dark">
            <b-tr>
                <b-th v-for="column in columns" :key="column">
                    {{ correctSpace(column) }}
                </b-th>
            </b-tr>
        </b-thead>
        <b-tbody>
            <b-tr v-for="data in datas">
                <b-td @click="column_click(column,data[column])" v-for="column in columns"
                      :class="getCellClasses(column,data[column])">

                    {{ data[column] }}
                </b-td>
            </b-tr>
        </b-tbody>
    </b-table-simple>
</template>
<script lang="ts">
import {Component, Emit, Prop, Vue} from "vue-property-decorator";

const space = require('to-space-case');

function isNumber(rowValue: any) {
    return !isNaN(+rowValue);
}

@Component({})

export default class FxTab extends Vue {
    correctSpace(st: string) {
        return space(st)
    }

    @Prop() columns!: string[]
    @Prop() datas!: { [key: string]: any }[]
    @Prop() instr!: string
    @Prop() table!: string

    column_click(column: string, value: string) {
        this.$emit("column_click", column, value);
    }

    getCellClasses(columnName: string, rowValue: any) {

        if (!isNumber(rowValue)) {
            return ["white", "h5"];
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

}
</script>