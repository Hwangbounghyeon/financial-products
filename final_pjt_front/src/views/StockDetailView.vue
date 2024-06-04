<template>
  <v-container class="fill-height pa-4 d-flex align-center justify-center">
    <v-row v-if="stockDetail.length" class="w-100">
      <v-col cols="12">
        <v-card class="mb-4 card-outline">
          <v-card-title class="headline text-center"> 주식 정보 </v-card-title>
          <v-card-subtitle class="subtitle text-center">
            {{ stockDetail[0].ticker_name }}
          </v-card-subtitle>
          <v-divider></v-divider>
          <v-card-text>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>종목 코드</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockDetail[0].ticker
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>날짜</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockData.date
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>시가</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockData.opening_price
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>고가</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockData.highest_price
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>저가</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockData.lowest_price
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>종가</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockData.closing_price
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>거래량</v-list-item-title>
                  <v-list-item-subtitle>{{
                    stockData.volume
                  }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>등락률</v-list-item-title>
                  <v-list-item-subtitle
                    >{{ stockData.fluctuation_rate }}%</v-list-item-subtitle
                  >
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="stockDetail.length" class="w-100">
      <v-col cols="12">
        <StockPlot />
      </v-col>
    </v-row>
    <v-row v-else class="w-100">
      <v-col cols="12">
        <v-alert type="info">주식 정보를 불러오는 중입니다...</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useStockStore } from "@/stores/stockStore";
import StockPlot from "@/components/StockPlot.vue";

const store = useStockStore();
const route = useRoute();
const stockDetail = ref([]);
const stockData = ref({});

onMounted(async () => {
  const ticker = route.params.ticker; // 경로에서 ticker를 추출
  await store.getStockDetail(ticker);
  stockDetail.value = store.stockDetail;

  if (stockDetail.value.length) {
    const targetDate = "2024-05-22";
    stockData.value =
      stockDetail.value[0].stock.find((stock) => stock.date === targetDate) ||
      {};
  }
});
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

.v-container {
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-outline {
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  width: 100%;
}

.headline {
  font-family: "JG";
  font-size: 24px;
  color: #5a3e36;
  margin-bottom: 10px;
}

.subtitle {
  font-family: "LGB";
  font-size: 18px;
  color: #5a3e36;
  margin-bottom: 10px;
}

.v-list-item-title {
  font-family: "LGB";
  font-weight: bold;
}

.v-list-item-subtitle {
  font-family: "LGB";
}

.mb-4 {
  margin-bottom: 20px;
}
</style>
