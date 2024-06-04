<template>
  <div>
    <SignUpView />
  </div>
  <div>
    <LogInView />
  </div>
  <div>
    <p>{{ userStore.user.pk }}</p>
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/userStore";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";

const userStore = useUserStore();
</script>

<style scoped></style>
