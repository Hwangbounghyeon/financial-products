<template>
  <v-app>
    <MainHeader />
    <v-main>
      <v-container class="main-content">
        <RouterView />
      </v-container>
    </v-main>
    <MainFooter />
    <img src="@/assets/chatbot.png" alt="챗봇" class="chatbot-button" @click="toggleChat"></img>
    <ChatBot v-if="isChatOpen" @close="isChatOpen = false" />
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import MainHeader from '@/components/MainHeader.vue';
import MainFooter from '@/components/MainFooter.vue';
import ChatBot from '@/components/ChatBot.vue';

const isChatOpen = ref(false);

const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value;
};
</script>

<style scoped>
@font-face {
  font-family: 'JG';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_231029@1.1/JalnanGothic.woff') format('woff');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'LGB';
  src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/2403-2@1.0/TTLaundryGothicB.woff2') format('woff2');
  font-weight: 700;
  font-style: normal;
}

html,
body {
  background-color: #f9f6ec;
  margin: 0;
  padding: 0;
  height: 100%;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.v-main {
  flex: 1;
}

.main-content {
  flex: 1;
  padding-bottom: 64px; /* Footer의 높이만큼 추가 패딩 */
}

.footer {
  background-color: #f9f6ec; /* 헤더와 같은 배경색 */
  padding: 20px 0;
  width: 100%;
  margin-top: auto;
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
  font-family: 'LGB';
  flex-direction: column;
  justify-content: center;
  padding-left: 20px;
}

.chatbot-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: transparent;
  z-index: 1000;
  width: 100px;
  height: 100px;
  padding: 0;
  border: none;
  box-shadow: none;
}

.chatbot-button .v-avatar {
  width: 100px;
  height: 100px;
}
</style>
