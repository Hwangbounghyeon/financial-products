<template>
  <v-list-item>
    <v-list-item-content>
      <v-list-item-title>{{ review.content }}</v-list-item-title>
      <v-list-item-subtitle
        >{{ review.user.username }} |
        {{ review.updated_at }}</v-list-item-subtitle
      >
    </v-list-item-content>
    <v-list-item-action class="ml-auto">
      <v-btn
        v-if="review.user.id === userStore.user.pk"
        color="red"
        small
        @click="store.deleteReview(review.deposit_product, review.id)"
      >
        삭제
      </v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script setup>
import { defineProps } from 'vue';
import { useProductStore } from '@/stores/productStore';
import { useUserStore } from '@/stores/userStore';

const props = defineProps({
  review: Object,
});

const store = useProductStore();
const userStore = useUserStore();
</script>

<style scoped>
.v-list-item-title {
  font-weight: bold;
}

.v-list-item-subtitle {
  color: gray;
}

.ml-auto {
  margin-left: auto;
}
</style>
