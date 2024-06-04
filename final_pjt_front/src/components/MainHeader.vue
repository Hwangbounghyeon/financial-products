<template>
  <header class="main-header">
    <v-container>
      <v-row class="logo-menu-row">
        <v-col class="logo-container" cols="2">
          <img :src="logoSrc" alt="Logo" class="logo" @click="goMain()" />
        </v-col>
        <v-col class="menu-container" cols="8">
          <div class="menu-row">
            <div
              v-for="(category, index) in categories"
              :key="index"
              class="menu-item-container"
            >
              <RouterLink :to="category.link" class="menu-btn leaf">
                {{ category.name }}
              </RouterLink>
            </div>
          </div>
        </v-col>
        <v-col class="user-menu" cols="2">
          <div v-if="!isLogin" class="user-buttons">
            <RouterLink :to="{ name: 'LogIn' }" class="user-btn"
              >로그인</RouterLink
            >
            <span class="separator">|</span>
            <RouterLink :to="{ name: 'SignUp' }" class="user-btn"
              >회원가입</RouterLink
            >
          </div>
          <div v-else class="user-buttons">
            <RouterLink
              :to="{ name: 'Profile', params: { username: store.user.pk } }"
              class="user-btn username"
            >
              {{ store.user.username }}
            </RouterLink>
            <span class="separator">|</span>
            <v-btn @click="store.logOut" class="user-btn">로그아웃</v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import logoSrc from "@/assets/LOGO.webp";
import { useUserStore } from "@/stores/userStore.js";
import { useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const store = useUserStore();
const router = useRouter();
const { isLogin } = storeToRefs(store);

const categories = ref([
  { name: "소개", link: "/" },
  { name: "상품", link: "/products" },
  { name: "커뮤니티", link: "/posts" },
  { name: "주식", link: "/stocks" },
  { name: "지도", link: "/map" },
  { name: "환율", link: "/exchange" },
]);

const goMain = function () {
  router.push({ name: "Main" });
};
</script>

<style scoped>
@font-face {
  font-family: "LGB";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2403-2@1.0/TTLaundryGothicB.woff2")
    format("woff2");
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: "JG";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_231029@1.1/JalnanGothic.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

html,
body {
  background-color: #f9f6ec;
  margin: 0;
  padding: 0;
  height: 100%;
}

.main-header {
  background-color: #f9f6ec;
  padding: 2px 0; /* 패딩을 최대한 줄임 */
  top: 0;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo-menu-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0; /* 마진 제거 */
}

.logo-container {
  text-align: left; /* 로고를 왼쪽에 배치 */
  padding: 0; /* 로고 컨테이너 패딩 제거 */
}

.logo {
  max-width: 230px; /* 로고 크기 조정 */
}

.menu-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-left: 100px; /* 로고와 메뉴 버튼 사이의 마진을 100px로 설정 */
}

.menu-row {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  white-space: nowrap; /* 메뉴 버튼이 가로로 나란히 배치되도록 함 */
}

.menu-item-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 80px; /* 메뉴 버튼들 사이 간격 더 벌리기 */
}

.menu-btn {
  font-size: 1.8rem;
  color: #5a3e36;
  font-family: "JG";
  text-decoration: none;
}

.user-menu {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.user-buttons {
  display: flex;
  align-items: center;
  position: absolute;
  top: 10px; /* 우상단 모서리에서 살짝 떨어지게 배치 */
  right: 10px;
}

.user-btn {
  font-size: 1rem;
  color: black;
  background-color: transparent;
  border: none;
  font-family: "JG";
  text-decoration: none;
  margin: 0 5px;
}

.user-btn.username {
  text-decoration: underline;
}

.v-application .v-btn {
  background-color: transparent !important;
  box-shadow: none !important;
  outline: none !important;
}
</style>
