<template>
    <b-form inline>
        <label class="sr-only" for="inline-form-input-name">Username</label>
        <b-form-input
                id="inline-form-input-name"
                class="mb-2 mr-sm-2 mb-sm-0"
                placeholder="Username"
                prepend="@"
                v-model="auth.username"
        ></b-form-input>

        <label class="sr-only" for="inline-form-input-password">Password</label>
        <b-input-group class="mb-2 mr-sm-2 mb-sm-0">
            <b-form-input type="password" id="inline-form-input-password"
                          v-model="auth.password"
            ></b-form-input>
        </b-input-group>

        <b-button variant="primary" >Save</b-button>
    </b-form>
</template>
<script lang="ts">

import {Component, ModelSync, Vue} from 'vue-property-decorator'
import {AuthCredentials} from "@/views/AuthCredentials";

@Component
export default class LoginForm extends Vue {
    @ModelSync('auth','input') readonly authCredentials!: AuthCredentials;

}
</script>