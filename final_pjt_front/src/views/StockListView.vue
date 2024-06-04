<template>
  <v-container class="fill-height pa-4">
    <v-row>
      <v-col cols="12">
        <h1>주식정보</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8">
        <v-text-field
          v-model="searchQuery"
          label="종목명 검색"
          class="search-bar"
          solo
          hide-details
        ></v-text-field>
      </v-col>
      <v-col cols="4" class="text-right">
        <v-btn class="search-btn" @click="searchStocks">검색</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="community-list">
          <v-list>
            <v-list-item>
              <v-row class="header-row">
                <v-col cols="4">종목코드</v-col>
                <v-col cols="4">종목명</v-col>
                <v-col cols="4">종가</v-col>
              </v-row>
            </v-list-item>
            <v-divider></v-divider>
            <v-list-item
              v-for="stock in filteredStocks"
              :key="stock.ticker"
              @click="goStock(stock.ticker)"
              class="stock-item"
            >
              <v-list-item-content>
                <v-row>
                  <v-col cols="4">{{ stock.ticker }}</v-col>
                  <v-col cols="4">{{ stock.ticker_name }}</v-col>
                  <v-col cols="4">
                    {{ getClosingPriceOnDate(stock.stock, "2024-05-22") }}
                  </v-col>
                </v-row>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useStockStore } from "@/stores/stockStore";
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const store = useStockStore();
const router = useRouter();
const searchQuery = ref("");

const headers = [
  { text: "종목코드", value: "ticker" },
  { text: "종목명", value: "ticker_name" },
  { text: "종가", value: "closing_price" },
];

const getClosingPriceOnDate = (stockList, targetDate) => {
  const stock = stockList.find((data) => data.date === targetDate);
  return stock ? stock.closing_price : "정보 없음";
};

onMounted(() => {
  store.getStocks();
});

const filteredStocks = computed(() => {
  if (!searchQuery.value) {
    return store.stocks;
  }
  return store.stocks.filter((stock) =>
    stock.ticker_name.includes(searchQuery.value)
  );
});

const searchStocks = () => {
  // 검색 로직을 구현합니다.
};

const goStock = (ticker) => {
  store.getStockDetail(ticker);
  router.push({ name: "StockDetail", params: { ticker: ticker } });
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
  font-family: "JG";
  margin-bottom: 16px;
}

.search-bar {
  background-color: white;
  border-radius: 8px;
  box-shadow: none;
  border: 1px solid #5a3e36;
  font-family: "JG";
}

.search-btn {
  font-family: "LGB";
  background-color: #f8f0d8;
  color: #5a3e36;
  border-radius: 8px;
  margin-right: 30px;
}

.community-list {
  max-height: 400px;
  overflow-y: auto;
}

.header-row {
  font-weight: bold;
  text-align: center;
  background-color: #f8f0d8;
  padding: 8px;
}

.stock-item:hover {
  background-color: #f5f5f5;
  cursor: pointer;
}

.stock-item {
  font-family: "LGB";
  text-align: center;
}

.v-list-item-content .v-row {
  display: flex;
  justify-content: center;
}

.v-list-item-content .v-col {
  text-align: center;
  padding: 8px;
  border-bottom: 1px solid #e0e0e0;
}
</style>
