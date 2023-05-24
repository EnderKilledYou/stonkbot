<template>
    <b-form inline>
        <label class="sr-only" for="inline-form-input-url">Backend Url</label>
        <b-form-input
                id="inline-form-input-url"
                class="mb-2 mr-sm-2 mb-sm-0"
                placeholder="Backend Url"

                v-model="auth.url"
        ></b-form-input>
        <label class="sr-only" for="inline-form-input-type">Connection Type</label>
        <b-form-input
                id="inline-form-input-type"
                class="mb-2 mr-sm-2 mb-sm-0"
                placeholder="Demo"

                v-model="auth.connectionType"
        ></b-form-input>
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
        <b-button-group>
            <b-button variant="primary" @click="LoginAttempt">Login</b-button>

            <b-button variant="danger" @click="ClearStorage">Reset Cookies for new version</b-button>
        </b-button-group>
    </b-form>
</template>
<script lang="ts">

import {Component, Emit, ModelSync, Vue} from 'vue-property-decorator'
import {AuthCredentials} from "@/views/AuthCredentials";

@Component
export default class LoginForm extends Vue {
    @ModelSync('auth', 'input') readonly authCredentials!: AuthCredentials;

    ClearStorage() {
        localStorage.clear()
        alert("cleared")
    }

    @Emit('login')
    LoginAttempt() {

    }
}
</script>