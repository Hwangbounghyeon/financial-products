<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>추천상품</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col
        v-for="product in store.recommendedProducts"
        :key="product.id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="product-card" @click="goProduct(product.id)">
          <v-card-title class="headline">{{
            product.fin_prdt_nm
          }}</v-card-title>
          <v-card-subtitle>{{ product.kor_co_nm }}</v-card-subtitle>
          <v-card-text class="card-content">
            <div>가입방법: {{ product.join_way }}</div>
            <br />
            <div>만기후 이자율: {{ product.mtrt_int }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useUserStore } from '@/stores/userStore';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const store = useUserStore();
const router = useRouter();

onMounted(() => {
  if (store.isLogin) {
    store.recommend();
  } else {
    router.push({ name: 'LogIn' });
  }
});

const goProduct = (id) => {
  router.push({ name: 'ProductDetail', params: { id: id } });
};
</script>

<style scoped>
.product-card {
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
  margin-bottom: 20px;
  height: 250px; /* 모든 카드의 높이를 동일하게 설정 */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.product-card:hover {
  background-color: #f5f5f5;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.v-card-title {
  font-weight: bold;
  color: #424242;
}

.v-card-subtitle {
  color: #757575;
}

.card-content {
  color: #616161;
  flex-grow: 1; /* 컨텐츠를 수직 방향으로 균등하게 배치 */
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
