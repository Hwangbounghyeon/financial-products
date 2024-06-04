<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-row align="center" justify="center">
      <v-col cols="12" md="6">
        <v-card class="pa-6 card-outline">
          <v-card-title class="headline text-center">
            <img :src="logoSrc" alt="IPPARI" class="logo" />
          </v-card-title>

          <v-card-text>
            <v-form @submit.prevent="signUp">
              <v-text-field
                v-model.trim="username"
                label="이름"
                outlined
                dense
                required
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="nick_name"
                label="닉네임"
                outlined
                dense
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="email"
                label="이메일"
                outlined
                dense
                type="email"
                required
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="age"
                label="나이"
                outlined
                dense
                type="number"
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="password1"
                label="비밀번호"
                outlined
                dense
                type="password"
                required
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="password2"
                label="비밀번호 확인"
                outlined
                dense
                type="password"
                required
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="salary"
                label="봉급"
                outlined
                dense
                type="number"
                class="text-field"
              ></v-text-field>

              <v-text-field
                v-model.trim="money"
                label="자산"
                outlined
                dense
                type="number"
                class="text-field"
              ></v-text-field>

              <v-file-input
                v-model="img"
                label="프로필 이미지"
                outlined
                dense
                class="text-field"
              ></v-file-input>

              <v-btn
                type="submit"
                color="#a3d5ff"
                class="ma-2 submit-btn"
                block
              >
                가입하기
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/userStore.js";
import logoSrc from "@/assets/FLOGO.webp";

const store = useUserStore();
const username = ref("");
const password1 = ref("");
const password2 = ref("");
const email = ref("");
const nick_name = ref("");
const age = ref(null);
const money = ref(null);
const salary = ref(null);
const img = ref(null);

const signUp = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
    nick_name: nick_name.value,
    age: age.value,
    money: money.value,
    salary: salary.value,
    img: img.value,
  };
  store.signUp(payload);
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
  width: 600px;
  margin-left: 130px; /* 추가된 부분 */
}

.logo {
  max-width: 200px;
  margin: 0 auto 20px;
}

.headline {
  font-family: "JG";
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.text-field {
  margin-bottom: 16px;
  font-family: "JG";
}

.submit-btn {
  background-color: #5a3e36;
  color: #fff;
  border-radius: 8px;
  font-family: "LGB";
}

.v-text-field input {
  font-family: "JG";
}

.v-text-field input::placeholder {
  font-family: "JG";
}
</style>
