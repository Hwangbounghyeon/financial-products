<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-row align="center" justify="center" class="w-100">
      <v-col cols="12" md="8">
        <v-card class="pa-6 card-outline">
          <v-card-title class="headline text-center">
            <h1>{{ profileUser.username }}님의 프로필</h1>
          </v-card-title>
          <v-card-subtitle class="subtitle text-center">
            <h2>수정할 정보를 입력하세요.</h2>
          </v-card-subtitle>
          <v-card-text>
            <v-row class="profile-row">
              <v-col cols="12" class="profile-info-col">
                <v-form @submit.prevent="updateProfile">
                  <v-text-field
                    v-model="username"
                    label="이름"
                    outlined
                    dense
                    class="text-field"
                  ></v-text-field>
                  <v-text-field
                    v-model="nick_name"
                    label="닉네임"
                    outlined
                    dense
                    class="text-field"
                  ></v-text-field>
                  <v-text-field
                    v-model="age"
                    label="나이"
                    type="number"
                    outlined
                    dense
                    class="text-field"
                  ></v-text-field>
                  <v-text-field
                    v-model="email"
                    label="이메일"
                    type="email"
                    outlined
                    dense
                    class="text-field"
                  ></v-text-field>
                  <v-text-field
                    v-model="money"
                    label="자산"
                    type="number"
                    outlined
                    dense
                    class="text-field"
                  ></v-text-field>
                  <v-text-field
                    v-model="salary"
                    label="연봉"
                    type="number"
                    outlined
                    dense
                    class="text-field"
                  ></v-text-field>
                  <div class="profile-buttons">
                    <v-btn type="submit" class="profile-btn save-btn"
                      >저장</v-btn
                    >
                    <RouterLink
                      :to="{
                        name: 'Profile',
                        params: { username: store.user.pk },
                      }"
                    >
                      <v-btn class="profile-btn cancel-btn">취소</v-btn>
                    </RouterLink>
                    <v-btn
                      class="profile-btn drop-out-btn"
                      @click="store.dropOut"
                      >회원 탈퇴</v-btn
                    >
                  </div>
                </v-form>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import { useUserStore } from "@/stores/userStore";
import { storeToRefs } from "pinia";

const store = useUserStore();
const { profileUser } = storeToRefs(store);
const route = useRoute();
const username = ref(null);
const email = ref(null);
const nick_name = ref(null);
const age = ref(null);
const money = ref(null);
const salary = ref(null);

onMounted(() => {
  const user = store.profileUser;
  username.value = user.username;
  email.value = user.email;
  nick_name.value = user.nickname; // 변수명 수정
  age.value = user.age;
  money.value = user.money;
  salary.value = user.salary;
});

const updateProfile = () => {
  const payload = {
    username: username.value,
    email: email.value,
    nickname: nick_name.value, // 변수명 수정
    age: age.value,
    money: money.value,
    salary: salary.value,
  };
  console.log(payload);
  const id = route.params.pk;
  store.updateUser(id, payload);
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

.subtitle {
  font-family: "JG";
  font-size: 20px;
  color: #666;
  margin-bottom: 20px;
}

.profile-row {
  font-family: "LGB";
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.profile-info-col {
  max-width: 600px;
}

.text-field {
  margin-bottom: 16px;
  font-family: "JG";
}

.profile-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.profile-btn {
  width: auto;
  margin: 5px;
  font-size: 1rem;
  font-weight: bold;
}

.save-btn {
  background-color: #a3d5ff;
  color: #fff;
}

.cancel-btn {
  background-color: #b0b0b0;
  color: #fff;
}

.drop-out-btn {
  background-color: #ffa3a3;
  color: #fff;
}
</style>
