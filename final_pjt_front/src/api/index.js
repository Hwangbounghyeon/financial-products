import axios from "axios";
import { useUserStore } from "@/stores/userStore";

// 기본 URL로 사용하기 위한 BASE_URL
const BASE_URL = "http://localhost:8000";

// GET 요청 시 사용할 api(axios 대신 사용 가능)
const api = axios.create({
  baseURL: BASE_URL,
});

// PUT(PATCH), POST, DELETE 요청 시 사용할 api(axios 대신 사용 가능)
const authApi = axios.create({
  baseURL: BASE_URL,
});

// request와 response 사이에서 공통되게 로직을 처리
authApi.interceptors.request.use((config) => {
  const userStore = useUserStore();
  // 만약 로그인이 되어 있는 상태라면
  // Authorization 헤더에 토큰을 담는다.
  if (userStore.isLogin) {
    config.headers.Authorization = `Token ${userStore.token}`;
  }
});

// 외부에서 사용할 수 있게 export
export { api, authApi };
