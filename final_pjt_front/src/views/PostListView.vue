<template>
  <v-container style="height: 897.6px">
    <h1>커뮤니티</h1>
    <v-row>
      <v-col cols="8">
        <v-text-field
          v-model="searchQuery"
          placeholder="제목 검색"
          class="search-bar"
          solo
          color="olive"
          hide-details
        ></v-text-field>
      </v-col>
      <v-col cols="4" class="text-right">
        <v-btn class="search-btn" @click="goCreate">게시글 작성</v-btn>
      </v-col>
    </v-row>
    <v-data-table
      class="community-table"
      :items-per-page="itemsPerPage"
      :hide-default-footer="true"
    >
      <thead>
        <tr>
          <th class="table-header">작성 시간</th>
          <th class="table-header table-header-author">작성자</th>
          <th class="table-header table-header-title">제목</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="community in paginatedPosts"
          :key="community.id"
          @click="goToPost(community.key)"
        >
          <td class="table-cell">{{ formatDate(community.created_at) }}</td>
          <td class="table-cell">{{ community.user.username }}</td>
          <td class="table-cell">{{ community.title }}</td>
        </tr>
      </tbody>
    </v-data-table>
    <div class="pagination-controls">
      <v-btn icon @click="prevPage" :disabled="currentPage === 1">
        <v-icon>mdi-chevron-left</v-icon>
      </v-btn>
      <v-select
        v-model="currentPage"
        :items="pageNumbers"
        class="page-select"
        dense
        hide-details
        label=""
        :menu-props="{ contentClass: 'text-center' }"
        style="max-width: 100px; margin: 0 16px"
      ></v-select>
      <v-btn icon @click="nextPage" :disabled="currentPage === totalPages">
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </div>
  </v-container>
</template>

<script setup>
import { useComStore } from "@/stores/communityStore";
import { useUserStore } from "@/stores/userStore";
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const store = useComStore();
const userStore = useUserStore();
const router = useRouter();
const searchQuery = ref("");
const currentPage = ref(1);
const itemsPerPage = 10;

onMounted(() => {
  store.getPosts();
});

const goCreate = () => {
  if (userStore.isLogin) {
    router.push({ name: "PostCreateView" });
  } else {
    router.push({ name: "LogIn" });
  }
};

const filteredPosts = computed(() => {
  let posts = store.posts.slice().sort((a, b) => b.key - a.key); // 내림차순 정렬
  if (!searchQuery.value) {
    return posts;
  }
  return posts.filter((post) => post.title.includes(searchQuery.value));
});

const paginatedPosts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredPosts.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredPosts.value.length / itemsPerPage);
});

const pageNumbers = computed(() => {
  return Array.from({ length: totalPages.value }, (_, i) => i + 1);
});

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const goToPost = (id) => {
  router.push({ name: "PostDetail", params: { id: id } });
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

h1 {
  color: #5a3e36;
  font-family: JG;
  margin-bottom: 16px;
}

.search-bar {
  background-color: white;
  border-radius: 8px;
  box-shadow: none;
  border: 1px solid #5a3e36;
  font-family: "JG";
}

.search-btn {
  font-family: "LGB";
  background-color: #f8f0d8; /* olive green 계통의 파스텔 색 */
  color: #5a3e36;
  border-radius: 8px;
}

.community-table {
  font-family: LGB;
  width: 100%;
  margin-top: 16px;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
}

.table-header {
  background-color: #f8f0d8; /* 테이블 헤더를 어울리는 파스텔 색으로 설정 */
  padding: 16px;
  text-align: left;
  border-bottom: 2px solid #f8f0d8; /* 구분선 추가 */
}

.table-header-author {
  width: 20%;
}

.table-header-title {
  width: 50%;
}

.table-cell {
  padding: 30px;
  border-bottom: 1px solid #e0e0e0;
  text-align: left; /* 왼쪽 정렬 */
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 16px;
}

.page-select .v-select__selections {
  justify-content: center;
  text-align: center;
}
</style>
