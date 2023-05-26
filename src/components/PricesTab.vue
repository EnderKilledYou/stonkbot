<template>
    <div>
        <div v-for="instr in selectedInstrs">

            <prices-tab-instance :amount="amount" :auth="auth"  :instr="instr"
                         :table="table" class="mx-4 my-4"/>
        </div>
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

export default class PricesTab extends Vue {
    @Prop({default: ''}) table!: string;
    @Prop() instr!: string;
    @Prop() selectedInstrs!: string[];
    @Prop() auth!: AuthCredentials;
    amount: number = 0





}
</script>