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
            <b-tr v-for="data in datas" :key="data['instrument']">
                <b-td @click="cell_click(column,data[column],data)" v-for="column in columns" :key="column"
                      :class="getCellClasses(column,data[column])">
                    <b-button variant="primary" v-if="IsButtonColumn(column)">
                        {{ getButtonColumnText(column) }}
                        {{ data[column] }}

                    </b-button>
                    <p v-else>{{ data[column] }}</p>

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

    @Prop({default: ()=>[]}) button_columns!: { [key: string]: any }[];
    @Prop() columns!: string[]
    @Prop() datas!: { [key: string]: any }[]
    @Prop() instr!: string
    @Prop() table!: string

    getButtonColumnText(column: string) {
        const butCol = this.getButtonColumn(column);
        if (!butCol) return "";
        if ('column_text' in butCol)
            return "";
        return butCol['column_text']

    }

    IsButtonColumn(column: string) {
        debugger
        return this.getButtonColumn(column);
    }

    private getButtonColumn(column: string) {
        for (const butCol of this.button_columns) {
            if (butCol['column'] === column)
                return butCol;
        }
        return null;
    }

    cell_click(column: string, value: string, row: any) {
        this.$emit("cell_click", column, value, row);
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