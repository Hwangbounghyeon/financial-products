<template>
  <v-footer class="footer" padless>
    <v-container>
      <v-row class="footer-row">
        <v-col class="logo-container" cols="2">
          <img :src="logoSrc" alt="Logo" class="logo" />
        </v-col>
        <v-col class="info-container" cols="10">
          <div class="info-row">
            <h3>
              대표: 김호경 | 연락처: 010 - 2828 - 1003 | e-mail:
              jinglove@ssafy.kr
            </h3>
            <h3>
              대표: 황병헌 | 연락처: 010 - 2828 - 9999 | e-mail:
              inelove@ssafy.kr
            </h3>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup>
import logoSrc from "@/assets/FLOGO.webp"; // 로고 이미지 경로
</script>

<style scoped>
.footer {
  background-color: #f9f6ec; /* 헤더와 같은 배경색 */
  padding: 20px 0;
  width: 100%;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.footer-row {
  display: flex;
  align-items: center;
}

.logo-container {
  text-align: center;
}

.logo {
  max-width: 150px;
}

.info-container {
  display: flex;
  align-items: center;
}

.info-row {
  display: flex;
  font-family: "LGB";
  flex-direction: column;
  justify-content: center;
  padding-left: 20px;
}
</style>
