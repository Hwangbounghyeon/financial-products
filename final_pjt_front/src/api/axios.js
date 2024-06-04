import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Django 서버의 URL
  withCredentials: true, // 세션 쿠키를 포함 (JWT에서는 필요 없음)
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default instance;
