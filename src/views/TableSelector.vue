<template>
    <b-form-group id="input-group-3" label="Table:" label-for="input-3">
        <b-form-select
                id="input-3"
                v-model="table_choice"
                :options="tables"
                required
        ></b-form-select>

    </b-form-group>
</template>
<script lang="ts">
import {Component,  Prop, PropSync, Vue} from "vue-property-decorator";
import ErrorMessage from "@/views/ErrorMessage.vue";
import TablePrinter from "@/views/TablePrinter.vue";
import LoginForm from "@/views/LoginForm.vue";
import {AuthCredentials} from "@/views/AuthCredentials";

@Component({
    components: {ErrorMessage},
})
export default class TableSelector extends Vue {
    @PropSync('table') readonly table_choice!: string;
    @Prop () tables!: string[];

}
</script>