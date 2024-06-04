<template>
  <div class="chatbot-container">
    <div class="chatbot-header">
      <h2>ChatBot</h2>
      <button @click="$emit('close')">X</button>
    </div>
    <div class="chatbot">
      <div class="messages">
        <strong>{{ 'BOT' }}:</strong>
        {{ '안녕하세요! 무엇을 도와드릴까요? :)' }}
        <div v-for="(message, index) in messages" :key="index" class="message">
          <strong>{{ message.sender }}:</strong> {{ message.text }}
        </div>
      </div>
      <input
        v-model="userMessage"
        @keyup.enter="sendMessage"
        placeholder="Type a message..."
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userMessage: '',
      messages: [],
    };
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === '') return;

      this.messages.push({ sender: 'User', text: this.userMessage });

      try {
        const response = await axios.post(
          'http://localhost:8000/chatbot/chat/',
          {
            message: this.userMessage,
          }
        );
        this.messages.push({ sender: 'Bot', text: response.data.response });
      } catch (error) {
        console.error('There was an error:', error);
      }

      this.userMessage = '';
    },
  },
};
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 300px;
  max-height: 400px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  display: flex;
  flex-direction: column;
}

.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #007bff;
  color: white;
}

.chatbot {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 10px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
}

.message {
  margin: 5px 0;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  width: 100%;
  box-sizing: border-box;
}
</style>
