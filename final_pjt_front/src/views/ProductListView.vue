<template>
  <v-container style="height: 897.6px">
    <h1>금융 상품</h1>
    <v-row>
      <v-col cols="4">
        <v-text-field
          label="상품 검색"
          v-model="searchQuery"
          class="search-bar"
          solo
          hide-details
        ></v-text-field>
      </v-col>
      <v-col cols="2">
        <v-select
          :items="bankList"
          label="은행선택"
          v-model="selectedBank"
          class="search-bar select-field"
        ></v-select>
      </v-col>
      <v-col cols="2">
        <v-select
          :items="depositTypes"
          label="예금적금타입"
          v-model="selectedDepositType"
          class="search-bar select-field"
        ></v-select>
      </v-col>
      <v-col cols="4" class="text-right">
        <v-btn @click="recommend" class="recommend-btn">추천받기</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="paginatedProducts"
          class="community-table"
          :hide-default-footer="true"
          :items-per-page="itemsPerPage"
          :footer-props="{
            itemsPerPageOptions: [5, 10, 15],
            showCurrentPage: true,
            itemsPerPageText: 'Items per page',
          }"
          :server-items-length="filteredProducts.length"
          fixed-header
          height="500px"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>상품 리스트</v-toolbar-title>
            </v-toolbar>
          </template>
          <template v-slot:header>
            <thead>
              <tr>
                <th
                  v-for="header in headers"
                  :key="header.value"
                  class="table-header"
                >
                  {{ header.text }}
                </th>
              </tr>
            </thead>
          </template>
          <template v-slot:item="{ item }">
            <tr @click="goDetail(item.id)" style="cursor: pointer">
              <td>{{ item.dcls_strt_day }}</td>
              <td>{{ item.kor_co_nm }}</td>
              <td>{{ item.fin_prdt_nm }}</td>
              <td>{{ item.save_trm_6m }}</td>
              <td>{{ item.save_trm_12m }}</td>
              <td>{{ item.save_trm_36m }}</td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <div class="pagination-controls">
      <v-btn icon @click="prevPage" :disabled="currentPage === 1">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-select
        v-model="currentPage"
        :items="pageNumbers"
        class="page-select"
        dense
        hide-details
        label=""
        :menu-props="{ contentClass: 'text-center' }"
        style="max-width: 100px; margin: 0 16px"
      ></v-select>
      <v-btn icon @click="nextPage" :disabled="currentPage === totalPages">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { useProductStore } from "@/stores/productStore";
import { useUserStore } from "@/stores/userStore";
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const store = useProductStore();
const userStore = useUserStore();
const router = useRouter();
const depositTypes = ref(["전체", "예금", "적금"]);
const selectedBank = ref("");
const searchQuery = ref("");
const selectedDepositType = ref("");

const bankList = ref([
  "은행전체",
  "경남은행",
  "광주은행",
  "국민은행",
  "농협은행주식회사",
  "대구은행",
  "부산은행",
  "수협은행",
  "신한은행",
  "우리은행",
  "전북은행",
  "제주은행",
  "주식회사 카카오뱅크",
  "주식회사 케이뱅크",
  "중소기업은행",
  "토스뱅크 주식회사",
  "하나은행",
  "한국산업은행",
  "한국스탠다드차타드은행",
]);

const headers = [
  { text: "공시제출일", value: "dcls_strt_day" },
  { text: "금융회사명", value: "kor_co_nm" },
  { text: "금융상품명", value: "fin_prdt_nm" },
  { text: "6개월", value: "save_trm_6m" },
  { text: "12개월", value: "save_trm_12m" },
  { text: "36개월", value: "save_trm_36m" },
];

const currentPage = ref(1);
const itemsPerPage = 10;

onMounted(() => {
  store.getProducts();
});

const goDetail = function (id) {
  router.push({ name: "ProductDetail", params: { id: id } });
};

const filteredProducts = computed(() => {
  let products = store.products;

  if (selectedBank.value && selectedBank.value !== "은행전체") {
    products = products.filter(
      (product) => product.kor_co_nm === selectedBank.value
    );
  }

  if (searchQuery.value) {
    products = products.filter(
      (product) =>
        product.fin_prdt_nm.includes(searchQuery.value) ||
        product.kor_co_nm.includes(searchQuery.value)
    );
  }

  if (selectedDepositType.value && selectedDepositType.value !== "전체") {
    products = products.filter(
      (product) => product.type === selectedDepositType.value
    );
  }

  return products.map((product) => {
    const save_trm_6m =
      product.options?.find((option) => option.save_trm === "6")?.intr_rate2 ||
      "-";
    const save_trm_12m =
      product.options?.find((option) => option.save_trm === "12")?.intr_rate2 ||
      "-";
    const save_trm_36m =
      product.options?.find((option) => option.save_trm === "36")?.intr_rate2 ||
      "-";

    return {
      id: product.id,
      dcls_strt_day: product.dcls_strt_day,
      kor_co_nm: product.kor_co_nm,
      fin_prdt_nm: product.fin_prdt_nm,
      save_trm_6m: save_trm_6m,
      save_trm_12m: save_trm_12m,
      save_trm_36m: save_trm_36m,
    };
  });
});

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredProducts.value.slice(start, end);
});

const recommend = function () {
  if (userStore.isLogin) {
    router.push({ name: "Recommend" });
  } else {
    router.push({ name: "LogIn" });
  }
};

const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage);
});

const pageNumbers = computed(() => {
  return Array.from({ length: totalPages.value }, (_, i) => i + 1);
});

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const formatDate = (date) => {
  const options = {
    year: "2-digit",
    month: "2-digit",
    day: "2-digit",
  };
  return new Date(date).toLocaleDateString("ko-KR", options);
};
</script>

<style scoped>
@font-face {
  font-family: "JG";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_231029@1.1/JalnanGothic.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: "LGB";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2403-2@1.0/TTLaundryGothicB.woff2")
    format("woff2");
  font-weight: 700;
  font-style: normal;
}

h1 {
  color: #5a3e36;
  font-family: JG;
  margin-bottom: 16px;
}

.search-bar {
  background-color: white;
  border-radius: 8px;
  box-shadow: none;
  border: 1px solid #5a3e36;
  font-family: "JG";
}

.select-field {
  margin-bottom: 16px;
}

.search-btn {
  font-family: "LGB";
  background-color: #f8f0d8;
  color: #5a3e36;
  border-radius: 8px;
}

.recommend-btn {
  background-color: #b0e0e6;
  color: white;
}

.community-table {
  font-family: LGB;
  width: 100%;
  margin-top: 16px;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  background-color: #f8f0d8;
  padding: 16px;
  text-align: left;
  border-bottom: 2px solid #f8f0d8;
  color: #5a3e36;
}

.table-header-author {
  width: 20%;
}

.table-header-title {
  width: 50%;
}

.table-cell {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  text-align: left;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 16px;
}

.page-select .v-select__selections {
  justify-content: center;
  text-align: center;
}
</style>
