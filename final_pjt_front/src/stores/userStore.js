import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useRouter } from 'vue-router';
import axios from 'axios';

axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
axios.defaults.xsrfCookieName = 'csrftoken';

export const useUserStore = defineStore(
  'user',
  () => {
    // user와 관련된 정보는 'accounts/'로 연결되기 때문에 baseurl 지정.
    const BASE_URL = 'http://localhost:8000/accounts';
    // user가 권한이 있을 시 token 값을 저장하기 위한 변수
    const token = ref(null);
    const router = useRouter();
    const recommendedProducts = ref(null);
    const financialProducts = ref(null);
    const user = ref({});
    const profileUser = ref(null);
    // user가 로그인 했다면 token 값이 있으므로 true 반환
    const isLogin = computed(() => {
      if (token.value) {
        return true;
      } else {
        return false;
      }
    });

    // user가 회원가입 하는 axios
    const signUp = (payload) => {
      const formData = new FormData();
      formData.append('username', payload.username);
      formData.append('email', payload.email);
      formData.append('password1', payload.password1);
      formData.append('password2', payload.password2);
      formData.append('nick_name', payload.nick_name);
      formData.append('financial_products', '');
      formData.append('salary', payload.salary);
      formData.append('age', payload.age);
      formData.append('money', payload.money);
      if (payload.img) {
        formData.append('img', payload.img);
      }

      axios({
        url: 'http://localhost:8000/accounts/register/',
        method: 'POST',
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((response) => {
          const username = payload.username;
          const password = payload.password1;
          logIn({ username, password });
          router.push({ name: 'Main' });
        })
        .catch((error) => {
          alert('중복되는 값이 있습니다.');
          console.log(error);
        });
    };

    // user가 로그인 하는 axios
    const logIn = (payload) => {
      // 외부에서 호출할 때, then 구문을 사용하기 위한 return
      axios({
        url: `${BASE_URL}/login/`,
        method: 'POST',
        data: {
          username: payload.username,
          password: payload.password,
        },
      })
        .then((response) => {
          token.value = response.data.key;
          // then 구문으로 이동하기 싫다면 아래처럼 사용.
          loadUser();
          router.push({ name: 'Main' });
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const changePassword = function (payload) {
      axios({
        url: `${BASE_URL}/change_password/`,
        method: 'POST',
        data: {
          username: payload.username,
          old_password: payload.old_password,
          new_password1: payload.new_password1,
          new_password2: payload.new_password2,
        },
      });
    };

    // 로그아웃 함수
    const logOut = function () {
      axios({
        url: `${BASE_URL}/logout/`,
        method: 'POST',
        headers: {
          'X-CSRFToken': token.value,
        },
        withCredentials: true,
      })
        .then((response) => {
          clear();
          router.push({ name: 'Main' });
        })
        .catch((error) => {
          console.log(error);
        });
    };

    // 회원탈퇴 함수
    const dropOut = function () {
      axios({
        method: 'DELETE',
        url: `http://localhost:8000/accounts/dropout/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((response) => {
          // 회원탈퇴 성공 시 처리
          router.push({ name: 'Main' }); // 홈 페이지로 리디렉션
        })
        .catch((error) => {
          console.error('Delete user error:', error);
        });
    };

    // 상품가입 함수
    const toggleProduct = async function (pk) {
      axios({
        method: 'POST',
        url: `${BASE_URL}/toggle-financial-product/${pk}/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      }).then((response) => {
        console.log(response.data);
        alert(`상품을 ${response.data.action}하였습니다.`);
      });
    };

    // 프로필 함수
    const profile = async function (pk) {
      try {
        const response = await axios.get(`${BASE_URL}/${pk}/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });
        console.log(response.data);
        profileUser.value = response.data;
        loadFinancialProducts(pk);
      } catch (error) {
        console.error('Error fetching product detail:', error);
      }
    };

    // 회원수정 함수
    const updateUser = (id, payload) => {
      const formData = new FormData();
      formData.append('username', payload.username);
      formData.append('email', payload.email);
      // formData.append('password1', payload.password1);
      // formData.append('password2', payload.password2);
      formData.append('nick_name', payload.nick_name);
      // formData.append('financial_products', payload.financial_products);
      formData.append('salary', payload.salary);
      formData.append('age', payload.age);
      formData.append('money', payload.money);
      // if (payload.img) {
      //   formData.append('img', payload.img);
      // }
      axios({
        method: 'PUT',
        url: `${BASE_URL}/${id}/`,
        data: formData,
        headers: {
          Authorization: `Token ${token.value}`,
          'Content-Type': 'multipart/form-data',
        },
      })
        .then((response) => {
          router.push({ name: 'Profile', params: { username: id } });
        })
        .catch((error) => {
          console.error('Failed to update User:', error);
        });
    };

    // 사용자 불러오는 함수
    const loadUser = async function () {
      try {
        const response = await axios.get(
          'http://localhost:8000/accounts/user/',
          {
            headers: {
              Authorization: `Token ${token.value}`,
            },
          }
        );
        user.value = response.data;
      } catch (error) {
        console.error('사용자 정보 요청 실패:', error);
      }
    };

    // 추천상품 함수
    const recommend = async function () {
      try {
        const response = await axios.get(`${BASE_URL}/recommend/`, {
          headers: {
            Authorization: `Token ${token.value}`,
          },
        });
        recommendedProducts.value = response.data;
      } catch (error) {
        recommendedProducts.value = null;
        console.error('Error fetching recommendations:', error);
      }
    };

    // 사용자가 가입한 상품 함수
    const loadFinancialProducts = function (pk) {
      axios({
        method: 'GET',
        url: `${BASE_URL}/${pk}/signupproduct/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
        .then((response) => {
          financialProducts.value = response.data;
        })
        .catch((err) => {
          financialProducts.value = null;
          console.error('Error loading financial products:', error);
        });
    };

    // 로그아웃, 회원탈퇴 시 token 값을 지우기 위한 함수
    const clear = () => {
      token.value = '';
      recommendedProducts.value = null;
      financialProducts.value = null;
      user.value = null;
      profileUser.value = null;
    };

    return {
      BASE_URL,
      token,
      signUp,
      dropOut,
      logIn,
      logOut,
      clear,
      isLogin,
      changePassword,
      recommendedProducts,
      recommend,
      loadUser,
      user,
      profile,
      profileUser,
      toggleProduct,
      updateUser,
      loadFinancialProducts,
      financialProducts,
    };
  },
  { persist: true }
);
