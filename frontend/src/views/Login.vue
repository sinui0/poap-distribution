<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>{{appName}}</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-btn @click.prevent="submitExternal('reddit')">Login with Reddit</v-btn>
              <v-btn @click.prevent="submitExternal('discord')">Login with Discord</v-btn>
            </v-card-text>
            <v-card-text>
              <v-form @keyup.enter="submit">
                <v-text-field @keyup.enter="submit" v-model="email" prepend-icon="person" name="login" label="Login" type="text"></v-text-field>
                <v-text-field @keyup.enter="submit" v-model="password" prepend-icon="lock" name="password" label="Password" id="password" type="password"></v-text-field>
              </v-form>
              <div v-if="loginError.error">
                <v-alert :value="loginError" @loginError: transition="fade-transition" type="error">
                  {{loginError.detail}}
                </v-alert>
              </div>
              <v-flex class="caption text-xs-right"><router-link to="/recover-password">Forgot your password?</router-link></v-flex>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Pizzly from 'pizzly-js';
import { api } from '@/api';
import { appName } from '@/env';
import { readLoginError } from '@/store/main/getters';
import { dispatchLogIn, dispatchLogInExternal } from '@/store/main/actions';

const pizzly = new Pizzly({ host: 'localhost:8081' });
const myAPI = pizzly.integration('reddit');

@Component
export default class Login extends Vue {
  public email: string = '';
  public password: string = '';
  public appName = appName;

  public get loginError() {
    return readLoginError(this.$store);
  }

  public submit() {
    dispatchLogIn(this.$store, {username: this.email, password: this.password});
  }

  public submitExternal(providerName: string) {
    dispatchLogInExternal(this.$store, {providerName});
  }
}
</script>

<style>
</style>
