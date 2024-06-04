<template>
  <div>
    <v-container
      class="fill-height d-flex align-center justify-center"
      v-if="profileUser"
    >
      <v-row align="center" justify="center" class="w-100">
        <v-col cols="12" md="8">
          <v-card class="pa-6 card-outline">
            <v-card-title class="headline text-center">
              <h1>{{ profileUser.username }}님의 프로필</h1>
            </v-card-title>
            <v-card-text>
              <v-row class="profile-row">
                <v-col cols="4" class="profile-image-col">
                  <div class="profile-image">프로필 사진</div>
                  <div class="profile-buttons">
                    <v-btn
                      class="profile-btn join-product-btn"
                      @click="joinProduct"
                      >가입 상품</v-btn
                    >
                    <v-btn
                      class="profile-btn update-profile-btn"
                      @click="goUpdate"
                      >프로필 수정</v-btn
                    >
                    <v-btn
                      class="profile-btn drop-out-btn"
                      @click="store.dropOut"
                      >회원 탈퇴</v-btn
                    >
                  </div>
                </v-col>
                <v-col cols="8" class="profile-info-col">
                  <div class="personal-info">
                    <h3>개인 정보</h3>
                    <p>닉네임: {{ profileUser.nickname }}</p>
                    <p>나이: {{ profileUser.age }}</p>
                    <p>이메일: {{ profileUser.email }}</p>
                  </div>
                  <div class="asset-info">
                    <h3>자산 정보</h3>
                    <p>자산: {{ profileUser.money }}</p>
                    <p>연봉: {{ profileUser.salary }}</p>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-container v-else class="fill-height d-flex align-center justify-center">
      <v-skeleton-loader type="card" />
    </v-container>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/userStore";
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { storeToRefs } from "pinia";

const store = useUserStore();
const router = useRouter();
const route = useRoute();
const { profileUser } = storeToRefs(store);
const props = defineProps({
  username: Number,
});

onMounted(async () => {
  console.log(route.params);
  const username = route.params.username;
  store.loadUser();
  await store.profile(username);
});

const goUpdate = () => {
  router.push({ name: "UpdateUser", params: { pk: store.user.pk } });
};

const joinProduct = () => {
  // 가입 상품 로직
};
</script>

<style scoped>
@font-face {
  font-family: "JG";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_231029@1.1/JalnanGothic.woff")
    format("woff");
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: "LGB";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/2403-2@1.0/TTLaundryGothicB.woff2")
    format("woff2");
  font-weight: 700;
  font-style: normal;
}

.v-container {
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-outline {
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  width: 100%;
}

.headline {
  font-family: "JG";
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.profile-row {
  font-family: "LGB";
  display: flex;
  align-items: flex-start;
  margin-top: 20px;
}

.profile-image-col {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  color: #888;
  margin-bottom: 20px;
}

.profile-buttons {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.profile-btn {
  width: auto;
  margin: 5px;
  font-size: 1rem;
  font-weight: bold;
}

.join-product-btn {
  background-color: #a3d5ff;
  color: #fff;
}

.update-profile-btn {
  background-color: #ffc1a3;
  color: #fff;
}

.drop-out-btn {
  background-color: #ffa3a3;
  color: #fff;
}

.profile-info-col {
  font-family: "LGB";
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-left: 20px;
}

.personal-info,
.asset-info {
  margin-top: 20px;
  padding: 20px;
  background-color: #f9f6ec;
  border-left: 2px solid #ddd;
  border-radius: 8px; /* 모서리를 둥글게 */
}

.personal-info:not(:first-of-type),
.asset-info:not(:first-of-type) {
  margin-top: 30px; /* 각 창간의 간격을 벌려줌 */
}

.personal-info h3,
.asset-info h3 {
  margin-top: 0;
}

.personal-info p,
.asset-info p {
  margin: 5px 0;
}
</style>
