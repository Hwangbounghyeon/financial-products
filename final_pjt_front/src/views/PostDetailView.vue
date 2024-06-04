<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>{{ community?.title }}</h1>
        <p class="post-meta">
          작성자: {{ community?.user?.username }} | 작성시간:
          {{ formatDate(community?.updated_at) }}
        </p>
        <v-divider></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="content-area">
        <p>{{ community?.content }}</p>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="text-right">
        <v-btn
          v-if="community?.user?.username === user?.username"
          @click="updateCommunity"
          color="#B0E0E6"
          small
        >
          수정
        </v-btn>
        <v-btn
          v-if="community?.user?.username === user?.username"
          @click="deleteCommunity"
          color="#F08080"
          small
        >
          삭제
        </v-btn>
      </v-col>
    </v-row>
    <v-divider style="margin-bottom: 5px"></v-divider>
    <v-row>
      <v-col cols="12">
        <h2 class="comment-heading">댓글</h2>
        <div class="comment-list-container">
          <v-list
            class="comment-list"
            v-for="comment in paginatedComments"
            :key="comment.pk"
          >
            <v-list-item-content>
              <v-list-item-title>{{ comment.content }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ comment.user.username }} |
                {{ formatDate(comment.updated_at) }}
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action v-if="user?.username === comment.user.username">
              <v-btn color="error" small @click="deleteComment(comment.key)">
                삭제
              </v-btn>
            </v-list-item-action>
          </v-list>
        </div>
        <v-form @submit="createComment" class="comment-form">
          <v-text-field
            v-model="comment"
            placeholder="내용을 입력해주세요"
            required
            hide-details
          ></v-text-field>
          <v-btn type="submit" class="submit-btn">등록</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useComStore } from "@/stores/communityStore";
import { useUserStore } from "@/stores/userStore";
import { ref, onMounted, computed, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const community = ref(null);
const store = useComStore();
const userStore = useUserStore();
const comment = ref("");

const user = userStore.user;

const currentCommentPage = ref(1);
const commentsPerPage = 5;

onMounted(async () => {
  const id = route.params.id;
  community.value = await store.getPostDetail(id);
  userStore.loadUser();
});

const createComment = async () => {
  const id = route.params.id;
  const payload = {
    content: comment.value,
    community: id,
  };
  await store.createComment(id, payload);
  comment.value = "";
  await loadComments();
  nextTick(() => {
    scrollToCommentForm();
  });
};

const deleteComment = async (commentId) => {
  const id = route.params.id;
  try {
    await store.deleteComment(id, commentId);
    await loadComments();
  } catch (error) {
    console.error("댓글 삭제 실패:", error);
  }
};

const deleteCommunity = async () => {
  const id = route.params.id;
  try {
    await store.deletePost(id);
    router.push({ name: "PostList" });
  } catch (error) {
    console.error("게시글 삭제 실패:", error);
  }
};

const updateCommunity = () => {
  const id = route.params.id;
  router.push({ name: "PostDetailUpdate", params: { id: id } });
};

const formatDate = (date) => {
  const options = {
    year: "2-digit",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  };
  return new Date(date)
    .toLocaleDateString("ko-KR", options)
    .replace(/\./g, ".");
};

const paginatedComments = computed(() => {
  const start = (currentCommentPage.value - 1) * commentsPerPage;
  const end = start + commentsPerPage;
  return community.value?.comments.slice(start, end) || [];
});

const totalCommentPages = computed(() => {
  return Math.ceil((community.value?.comments.length || 0) / commentsPerPage);
});

const loadComments = async () => {
  const id = route.params.id;
  community.value = await store.getPostDetail(id);
};

const scrollToCommentForm = () => {
  const commentForm = document.querySelector(".comment-form");
  if (commentForm) {
    commentForm.scrollIntoView({ behavior: "smooth" });
  }
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
  margin-top: 20px;
  height: 100vh;
  max-width: 900px;
  margin: 0 auto;
  border-radius: 8px;
  background-color: #f8f0d8; /* 바탕색을 맞추어줍니다. */
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.content-area {
  min-height: 100px; /* 본문 내용이 출력되는 곳의 최소 높이를 줄입니다 */
  display: flex;
  align-items: flex-start; /* 본문 내용이 위쪽에 출력되도록 설정 */
}

.post-meta {
  color: #5a3e36;
  font-family: JG;
  margin-top: 8px;
}

h1,
h2 {
  color: #5a3e36;
  font-family: JG;
}

p {
  font-family: LGB;
  color: #5a3e36;
}

.v-btn {
  font-family: "LGB";
  background-color: #f8f0d8; /* olive green 계통의 파스텔 색 */
  color: #5a3e36;
  border-radius: 8px;
  margin: 5px;
}

.text-right {
  text-align: right;
}

.v-text-field {
  background-color: white;
  border-radius: 8px;
  box-shadow: none;
  border: 1px solid #5a3e36;
  font-family: "JG";
}

.comment-list-container {
  flex: 1;
  overflow-y: auto; /* 댓글 목록에 스크롤 추가 */
  padding-bottom: 20px; /* 댓글 입력창과의 간격 */
}

.v-list-item {
  background-color: #f8f0d8; /* 댓글 출력 창의 배경색을 맞추어 줍니다. */
  border-bottom: 1px solid #e0e0e0; /* 댓글 간 구분선 추가 */
  border-radius: 8px;
  margin-bottom: 10px;
  padding: 10px;
}

.v-list-item-title {
  font-family: LGB;
  color: #5a3e36;
}

.v-list-item-subtitle {
  font-family: JG;
  color: #5a3e36;
}

.comment-heading {
  margin-bottom: 20px; /* 댓글 헤딩과 구분선 사이의 간격 추가 */
}

.comment-form {
  margin-top: 20px; /* 댓글 입력 칸과 댓글 출력 창 사이의 간격 추가 */
}

.submit-btn {
  background-color: #5a3e36; /* 등록 버튼 배경색 */
  color: #f8f0d8; /* 등록 버튼 글자색 */
}

.v-list {
  background-color: #f8f0d8;
}
</style>
