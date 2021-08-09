<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Manage Identities</div>
      </v-card-title>
      <v-data-table :headers="headers" :items="userIdentities">
        <template slot="items" slot-scope="props">
          <td>{{ props.item.provider }}</td>
          <td>{{ props.item.external_user_id }}</td>
          <td>{{ props.item.created }}</td>
          <td class="justify-center layout px-0">
            <div v-if="userIdentities.length > 1">
              <v-tooltip top>
                <span>Delete</span>
                <v-btn slot="activator" flat>
                  <v-icon>delete</v-icon>
                </v-btn>
              </v-tooltip>
            </div>
          </td>
        </template>
      </v-data-table>
      <v-card-actions>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Store } from 'vuex';
import { readUserIdentities } from '@/store/main/getters';
import { dispatchGetUserIdentities } from '@/store/main/actions';

@Component
export default class UserIdentities extends Vue {
  public headers = [
    {
      text: 'Provider',
      sortable: false,
      value: 'provider',
      align: 'left',
    },
    {
      text: 'User ID',
      sortable: false,
      value: 'external_user_id',
      align: 'left',
    },
    {
      text: 'Created',
      sortable: true,
      value: 'created',
      align: 'left',
    },
  ];

  get userIdentities() {
    return readUserIdentities(this.$store);
  }

  public async mounted() {
    await dispatchGetUserIdentities(this.$store);
  }
}
</script>
