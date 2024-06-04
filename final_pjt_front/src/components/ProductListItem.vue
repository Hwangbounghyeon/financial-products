<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title>{{ item.kor_co_nm }}</v-list-item-title>
      <v-list-item-subtitle>{{ item.fin_prdt_nm }}</v-list-item-subtitle>
    </v-list-item-content>
    <v-list-item-action>
      <v-btn icon @click="viewDetails(item)">
        <v-icon>mdi-eye</v-icon>
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  item: Object,
});

const viewDetails = (item) => {
  console.log('View details for:', item);
};
</script>

<style scoped></style>
