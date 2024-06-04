import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useStockStore = defineStore(
  'stock',
  () => {
    const BASE_URL = 'http://localhost:8000/stock';
    const stocks = ref([]);
    const stockDetail = ref(null);
    const forecastData = ref(null);

    // 주식 정보 가져오는 함수
    const getStocks = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/stocklist/`);
        stocks.value = response.data;
      } catch (error) {
        console.error('Error fetching stock list:', error);
      }
    };

    // 주식 상세 정보 가져오는 함수
    const getStockDetail = async (ticker) => {
      try {
        const response = await axios.get(`${BASE_URL}/${ticker}/`);
        stockDetail.value = response.data;
      } catch (error) {
        console.error('Error fetching stock detail:', error);
      }
    };

    // 예측 데이터 가져오는 함수
    const getForecastData = async (ticker) => {
      try {
        const response = await axios.get(`${BASE_URL}/${ticker}/plot/`);
        forecastData.value = response.data;
      } catch (error) {
        console.error('Error fetching forecast data:', error);
      }
    };

    return {
      stocks,
      stockDetail,
      forecastData,
      getStocks,
      getStockDetail,
      getForecastData,
    };
  },
  { persist: true }
);
