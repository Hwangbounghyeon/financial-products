<template>
  <v-carousel hide-delimiters height="500px" interval="5000" cycle>
    <v-carousel-item
      v-for="(slide, i) in slides"
      :key="i"
      @click="goToRoute(slide.route)"
    >
      <v-img :src="slide.src" height="100%">
        <template v-slot:placeholder>
          <v-row class="fill-height ma-0">
            <v-col class="d-flex align-center justify-center">
              <v-progress-circular
                indeterminate
                color="grey lighten-5"
              ></v-progress-circular>
            </v-col>
          </v-row>
        </template>
      </v-img>
    </v-carousel-item>
    <template v-slot:extension>
      <v-row class="carousel-indicators">
        <v-col
          v-for="(slide, i) in slides"
          :key="i"
          class="d-flex align-center justify-center"
        >
          <v-icon color="black" class="indicator-icon">{{ i + 1 }}</v-icon>
        </v-col>
      </v-row>
    </template>
  </v-carousel>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import testSrc from '@/assets/test.png';
import introduce from '@/assets/introduce.png';
import product from '@/assets/product.png';
import community from '@/assets/community.png';
import stock from '@/assets/stock.png';
import map from '@/assets/map.png';
import exchange from '@/assets/exchange.png';

const router = useRouter();

const slides = ref([
  { src: introduce, route: 'introduce' },
  { src: product, route: 'PostList' },
  { src: community, route: 'PostList' },
  { src: stock, route: 'StockList' },
  { src: map, route: 'Map' },
  { src: exchange, route: 'Exchange' },
]);

const goToRoute = (routeName) => {
  router.push({ name: routeName });
};
</script>

<style scoped>
.carousel-indicators {
  position: absolute;
  bottom: 10px; /* 사진 밑에 배치 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 5px;
}

.indicator-icon {
  background-color: rgba(0, 0, 0, 0.7); /* 더 어두운 배경색 */
  border-radius: 50%;
  padding: 5px;
}

.v-carousel .v-carousel__controls__item {
  background-color: transparent !important;
}

.v-carousel .v-carousel__controls__next,
.v-carousel .v-carousel__controls__prev {
  display: none;
}
</style>
