<template>
  <v-container class="pa-4 fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" md="10">
        <v-card class="pa-6" style="font-size: 1.25rem">
          <v-card-title class="headline" style="font-size: 1.75rem"
            >환율 계산기</v-card-title
          >
          <v-divider></v-divider>

          <v-row class="mt-4">
            <v-col cols="12" md="5">
              <v-select
                v-model="toCountry"
                :items="store.country"
                label="변경하고 싶은 통화"
                outlined
                dense
                style="font-size: 1.25rem"
              ></v-select>
            </v-col>
            <v-col cols="12" md="2" class="d-flex justify-center align-center">
            </v-col>
            <v-col cols="12" md="5">
              <v-select
                v-model="fromCountry"
                :items="store.country"
                label="기준 통화"
                outlined
                dense
                style="font-size: 1.25rem"
              ></v-select>
            </v-col>
          </v-row>

          <v-row class="mt-4">
            <v-col cols="12" md="5" class="d-flex justify-center align-center">
              <v-img
                :src="store.icon[toCountry]"
                alt="Flag"
                contain
                max-width="100"
                max-height="100"
                v-if="store.icon[toCountry]"
              ></v-img>
              <div class="ml-3">
                <div>{{ toCountry }}</div>
                <div>{{ store.exchange[toCountry] }}</div>
              </div>
            </v-col>
            <v-col cols="12" md="2" class="d-flex justify-center align-center">
              <v-btn
                @click.prevent="store.swapCountry"
                icon
                color="secondary"
                class="ma-2"
              >
                <v-icon large>mdi-swap-horizontal</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="12" md="5" class="d-flex justify-center align-center">
              <v-img
                :src="store.icon[fromCountry]"
                alt="Flag"
                contain
                max-width="100"
                max-height="100"
                v-if="store.icon[fromCountry]"
              ></v-img>
              <div class="ml-3">
                <div>{{ fromCountry }}</div>
                <div>{{ store.exchange[fromCountry] }}</div>
              </div>
            </v-col>
          </v-row>

          <v-row class="mt-4">
            <v-col cols="12" md="12">
              <v-text-field
                v-model="Money"
                label="금액 입력"
                outlined
                dense
                class="money-input"
                style="font-size: 1.25rem; border-radius: 8px"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-row class="mt-4">
            <v-col cols="12" class="d-flex justify-center">
              <v-btn
                @click.prevent="store.getExchangeRate"
                color="primary"
                class="ma-2"
                style="font-size: 1.25rem"
              >
                변경
              </v-btn>
            </v-col>
          </v-row>

          <v-row class="mt-4">
            <v-col cols="12" class="text-center">
              <v-card class="pa-4">
                <span v-if="!isSwap">
                  {{ store.Money }} {{ store.exchange[toCountry] }} =
                  {{ store.convertedMoney }} {{ store.exchange[fromCountry] }}
                </span>
                <span v-else>
                  {{ store.Money }} {{ store.exchange[toCountry] }} =
                  {{ store.tempConvertedMoney }}
                  {{ store.exchange[fromCountry] }}
                </span>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted } from "vue";
import { useExchangeStore } from "@/stores/exchangeStore";
import { storeToRefs } from "pinia";

const store = useExchangeStore();
const { fromCountry, toCountry, isSwap, Money } = storeToRefs(store);

onMounted(() => {
  localStorage.removeItem("exchangeRate");
  store.fetchCountryList();
  store.fetchCodeList();
  store.fetchExchange();
  store.fetchCountryIcons();
});
</script>

<style scoped>
.money-input {
  background-color: #f5f5f5;
  width: 100%;
}
</style>
