<template>
  <div>
    <li @click="goDetail(getCommunity.key)">
      {{ getCommunity.key }} - {{ getCommunity.title }} -
      {{ getCommunity.user.username }} -
      {{ getCommunity.updated_at }}
    </li>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
defineProps({ getCommunity: Object });

const goDetail = function (id) {
  router.push({ name: 'PostDetail', params: { id: id } });
};
</script>

<style scoped></style>
