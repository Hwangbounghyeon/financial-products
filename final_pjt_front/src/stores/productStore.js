import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import axios from 'axios';

export const useProductStore = defineStore(
  'product',
  () => {
    const userstore = useUserStore();
    const router = useRouter();
    const products = ref([]);
    const reviews = ref([]);
    const BASE_URL = 'http://localhost:8000/products';
    // let products = ref([]);

    const getProducts = function () {
      axios({
        method: 'GET',
        url: `${BASE_URL}/productlist/`,
      })
        .then((response) => {
          products.value = response.data;
        })
        .catch((err) => {
          console.error('Error fetching products:', error);
        });
    };
    // 상품 상세 정보 가져오는 함수
    const getProductDetail = async function (pk) {
      try {
        const response = await axios.get(`${BASE_URL}/${pk}/`);
        return response.data;
      } catch (error) {
        console.error('Error fetching product detail:', error);
      }
    };

    // 추천 상품 받아오는 함수
    const recommendProducts = function () {
      if (products.value.length > 0) {
        return products.value.slice(0, 5);
      }
      return [];
    };

    // 상품 검색하는 함수
    const searchProduct = function (query) {
      if (query) {
        return products.value.filter((product) =>
          product.name.toLowerCase().includes(query.toLowerCase())
        );
      }
      return products.value;
    };

    // 리뷰 목록 가져오는 함수
    const getReviews = async function (productId) {
      try {
        const response = await axios.get(`${BASE_URL}/${productId}/review/`);
        return response.data;
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    };

    // 리뷰 작성하는 함수
    const createReview = async function (productId, reviewData) {
      axios({
        method: 'POST',
        url: `${BASE_URL}/${productId}/review/`,
        data: {
          content: reviewData.content,
          deposit_product: reviewData.deposit_product,
        },
        headers: {
          Authorization: `Token ${userstore.token}`,
        },
      })
        .then((response) => {
          reviews.value.push(response.data);
        })
        .catch((err) => {
          console.error('Error creating review:', err);
        });
    };

    // 리뷰 수정하는 함수
    const updateReview = async function (productId, reviewId, reviewData) {
      try {
        const response = await axios.patch(
          `${BASE_URL}/${productId}/review/${reviewId}`,
          reviewData
        );
        const index = reviews.value.findIndex(
          (review) => review.id === reviewId
        );
        if (index !== -1) {
          reviews.value[index] = response.data;
        }
      } catch (error) {
        console.error('Error updating review:', error);
      }
    };

    // 리뷰 삭제하는 함수
    const deleteReview = async function (productId, reviewId) {
      try {
        await axios.delete(`${BASE_URL}/${productId}/review/${reviewId}`);
        reviews.value = reviews.value.filter(
          (review) => review.id !== reviewId
        );
        router.go();
      } catch (error) {
        console.error('Error deleting review:', error);
      }
    };

    return {
      products,
      reviews,
      getProducts,
      getProductDetail,
      recommendProducts,
      searchProduct,
      getReviews,
      createReview,
      updateReview,
      deleteReview,
    };
  },
  { persist: true }
);
