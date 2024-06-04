<template>
  <div class="chart-container">
    <h1>가입한 상품 금리</h1>
    <canvas id="financialProductsChart"></canvas>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useRouter, useRoute } from 'vue-router';
import Chart from 'chart.js/auto';
import axios from 'axios';

const store = useUserStore();
const router = useRouter();
const route = useRoute();

onMounted(async () => {
  // 백엔드 API로부터 데이터 가져오기
  const response = await axios.get(`${store.BASE_URL}/${store.user.pk}/plots/`);
  const data = response.data.data;

  const labels = data.map((item) => item.fin_prdt_nm);
  const savingsRates = data.map((item) => item.intr_rate);
  const preferredRates = data.map((item) => item.intr_rate2);

  const ctx = document
    .getElementById('financialProductsChart')
    .getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: '저축 금리',
          backgroundColor: 'skyblue',
          data: savingsRates,
        },
        {
          label: '최고 우대금리 금리',
          backgroundColor: 'lightgreen',
          data: preferredRates,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: '가입한 상품 금리',
        },
      },
      scales: {
        x: {
          ticks: {
            maxRotation: 45,
            minRotation: 45,
          },
        },
      },
    },
  });
});
</script>

<style scoped>
.chart-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

canvas {
  display: block;
  width: 100%;
  height: 400px;
}
</style>
