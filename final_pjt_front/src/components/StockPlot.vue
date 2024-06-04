<template>
  <v-card class="mb-4">
    <v-card-title>예측 시계열 데이터</v-card-title>
    <v-card-text>
      <div class="chart-container">
        <canvas id="stock-chart"></canvas>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useStockStore } from '@/stores/stockStore';
import Chart from 'chart.js/auto';
import axios from 'axios';

const store = useStockStore();
const route = useRoute();
const chartData = ref(null);
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: false,
      ticks: {
        callback: function (value) {
          return value.toFixed(2); // 소수점 두 자리까지 표시
        },
      },
    },
  },
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: '주식 예측 시계열 데이터',
    },
  },
});

const fetchForecastData = async (ticker) => {
  try {
    const response = await axios.get(
      `http://localhost:8000/stock/${ticker}/plot/`
    );
    const forecast = response.data;

    if (forecast && forecast.historical_data && forecast.forecast_data) {
      const labels = forecast.historical_data.map((data) => data.date);
      const historicalData = forecast.historical_data.map(
        (data) => data.closing_price
      );
      const forecastDates = forecast.forecast_data.forecast_dates;
      const forecastPrices = forecast.forecast_data.forecast_prices;

      const allData = [...historicalData, ...forecastPrices];
      const minY = Math.min(...allData);
      const maxY = Math.max(...allData);

      // y축의 최소값과 최대값 설정
      chartOptions.value.scales.y.min = Math.floor(minY / 10) * 10;
      chartOptions.value.scales.y.max = Math.ceil(maxY / 10) * 10;
      chartOptions.value.scales.y.ticks.stepSize = Math.ceil(
        (maxY - minY) / 10
      ); // stepSize를 최대값과 최소값에 맞추어 설정

      chartData.value = {
        labels: [...labels, ...forecastDates],
        datasets: [
          {
            label: 'Closing Price',
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: false,
            tension: 0.1,
            data: historicalData,
          },
          {
            label: 'Forecast Price',
            borderColor: 'rgb(54, 162, 235)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: false,
            tension: 0.1,
            data: new Array(historicalData.length - 1)
              .fill(null)
              .concat(forecastPrices),
          },
        ],
      };

      renderChart();
    } else {
      console.error('Unexpected data structure:', forecast);
    }
  } catch (error) {
    console.error('Error fetching forecast data:', error);
  }
};

const renderChart = () => {
  const ctx = document.getElementById('stock-chart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: chartData.value,
    options: chartOptions.value,
  });
};

onMounted(() => {
  const ticker = route.params.ticker; // 경로에서 ticker를 추출
  fetchForecastData(ticker);
});
</script>

<style scoped>
.chart-container {
  height: 600px; /* 원하는 높이로 설정 */
}

.mb-4 {
  margin-bottom: 20px;
}
</style>
