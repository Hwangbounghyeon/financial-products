<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>커뮤니티 수정</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-text>
            <v-form @submit.prevent="submitEdit">
              <v-text-field
                v-model="title"
                placeholder="제목"
                outlined
                required
              ></v-text-field>
              <v-textarea
                v-model="content"
                placeholder="내용"
                outlined
                required
              ></v-textarea>
              <v-btn type="submit" class="submit-btn">수정</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useComStore } from "@/stores/communityStore";

const route = useRoute();
const router = useRouter();
const store = useComStore();
const title = ref("");
const content = ref("");
const postId = route.params.id;

onMounted(async () => {
  const communityData = await store.getPostDetail(postId);
  title.value = communityData.title;
  content.value = communityData.content;
});

const submitEdit = async () => {
  const payload = {
    title: title.value,
    content: content.value,
  };
  await store.updatePost(postId, payload);
  router.push({ name: "PostDetailView", params: { id: postId } });
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

h1 {
  font-family: "JG";
  color: #5a3e36;
}

.v-text-field {
  background-color: none;
  color: #5a3e36;
  font-family: LGB;
}

.v-container {
  margin-top: 20px;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.v-card {
  background-color: #f8f0d8;
  padding: 20px;
}

.v-btn {
  margin-top: 20px;
  font-family: "JG";
  background-color: #5a3e36;
  color: #f8f0d8;
}
</style>
