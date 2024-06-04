import { api, authApi } from "@/api/index";

// 주식 종목 목록을 가져오는 함수
const getStocks = () => {
  return api({
    method: "GET",
    url: "/stock/stocklist/",
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 주식 상세 정보를 가져오는 함수
const getStockDetailApi = async (id) => {
  return api({
    method: "GET",
    url: `/stock/${id}/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

export { getStocks, getStockDetailApi };
