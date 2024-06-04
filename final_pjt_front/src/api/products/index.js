import { api, authApi } from "@/api/index";

// 금융 상품 목록을 가져오는 함수
const getProductsApi = async () => {
  return api({
    method: "GET",
    url: "/products/productlist/",
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 금융 상품 상세 정보를 가져오는 함수
const getProductDetailApi = async (id) => {
  return api({
    method: "GET",
    url: `/products/${id}/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 추천 금융 상품 목록을 가져오는 함수
const recommendProductsApi = async () => {
  return api({
    method: "GET",
    url: "/products/recommend/",
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 금융 상품 리뷰를 작성하는 함수
const createReviewApi = async (product) => {
  return authApi({
    method: "POST",
    url: `/products/${product.id}/review/`,
    data: {
      product: product.id,
      content: product.content,
      like: product.like,
    },
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.error(error);
    });
};

// 금융 상품 리뷰 목록을 가져오는 함수
const getReviewsApi = (product) => {
  return authApi({
    method: "GET",
    url: `/products/${product.id}/review/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.error(error);
    });
};

// 금융 상품 리뷰를 수정하는 함수
const updateReviewApi = async (product, review) => {
  return authApi({
    method: "PATCH",
    url: `/products/${product.id}/review/${review.id}/`,
    data: {
      product: product.id,
      content: review.content,
      like: review.like,
    },
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.error(error);
    });
};

// 금융 상품 리뷰를 삭제하는 함수
const deleteReviewApi = async (product, review) => {
  return authApi({
    method: "DELETE",
    url: `/products/${product.id}/review/${review.id}/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.error(error);
    });
};

export {
  getProductsApi,
  getProductDetailApi,
  recommendProductsApi,
  createReviewApi,
  getReviewsApi,
  updateReviewApi,
  deleteReviewApi,
};
