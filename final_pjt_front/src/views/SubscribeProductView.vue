<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>가입한 상품</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-list>
          <v-list-item
            v-for="product in store.financialProducts"
            :key="product.id"
            class="product-item"
          >
            <v-list-item-content>
              <v-list-item-title>{{ product.fin_prdt_nm }}</v-list-item-title>
              <v-list-item-subtitle>{{
                product.kor_co_nm
              }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <UserPlot />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useUserStore } from '@/stores/userStore';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import UserPlot from '@/components/UserPlot.vue';
import { api } from '@/api/index.js';

const store = useUserStore();
const router = useRouter();
const profileImg = ref('');

onMounted(async () => {
  store.loadUser();
  store.profile(store.user.pk);
  api({
    url: `/media/${store.profileUser.img}`,
    method: 'get',
    responseType: 'blob',
  })
    .then((response) => {
      profileImg.value = URL.createObjectURL(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>

<style scoped>
.v-container {
  margin-top: 20px;
}

.product-item {
  cursor: pointer;
  transition: background-color 0.3s;
}

.product-item:hover {
  background-color: #f5f5f5;
}
</style>
