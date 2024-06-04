<template>
  <v-container v-if="product">
    <v-row>
      <v-col cols="12">
        <h1>{{ product.fin_prdt_nm ? product.fin_prdt_nm : "없음" }}</h1>
        <h2>{{ product.kor_co_nm }}</h2>
        <v-divider class="mb-4"></v-divider>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title class="d-flex justify-space-between">
            <span>상품 정보</span>
            <v-btn @click="toggleProduct(product.id)" class="join-btn"
              >가입하기</v-btn
            >
          </v-card-title>
          <v-card-text>
            <v-list dense>
              <v-list-item v-for="(value, title) in productInfo" :key="title">
                <v-list-item-content>
                  <v-list-item-title>{{ title }}</v-list-item-title>
                  <v-list-item-subtitle
                    class="wrap-text"
                    :class="{ 'expanded-subtitle': isExpandableField(title) }"
                  >
                    {{ value }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title>이자율 정보</v-card-title>
          <v-card-text>
            <v-row>
              <v-col
                v-for="option in product.options"
                :key="option.save_trm"
                cols="12"
                md="6"
              >
                <v-card class="option-card">
                  <v-card-title
                    >유형: {{ option.intr_rate_type_nm }}</v-card-title
                  >
                  <v-card-subtitle
                    >저축 기간: {{ option.save_trm }}개월</v-card-subtitle
                  >
                  <v-card-text>
                    <div>이자율: {{ option.intr_rate }}%</div>
                    <div>우대 이자율: {{ option.intr_rate2 }}%</div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card class="mb-4">
          <v-card-title>댓글</v-card-title>
          <v-card-text>
            <v-form @submit="createReview">
              <v-text-field
                v-model="comment"
                label="댓글을 입력해주세요"
                required
              ></v-text-field>
              <v-btn type="submit" color="#a3d5ff" class="submit-btn"
                >작성</v-btn
              >
            </v-form>
            <v-list>
              <v-list-item v-for="review in reviews" :key="review.id">
                <v-list-item-content>
                  <v-list-item-title>{{ review.content }}</v-list-item-title>
                  <v-list-item-subtitle
                    >{{ review.user.username }} |
                    {{ review.updated_at }}</v-list-item-subtitle
                  >
                </v-list-item-content>
                <v-list-item-action
                  v-if="review.user.username === user.username"
                >
                  <v-btn color="#ffa3a3" small @click="deleteReview(review.id)"
                    >삭제</v-btn
                  >
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
  <v-container v-else>
    <v-row>
      <v-col cols="12">
        <v-skeleton-loader type="card" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useProductStore } from "@/stores/productStore";
import { useUserStore } from "@/stores/userStore";

const route = useRoute();
const productStore = useProductStore();
const userStore = useUserStore();
const product = ref(null);
const reviews = ref([]);
const comment = ref("");
const user = userStore.user;

const productInfo = ref({});

const expandableFields = ["특별조건", "기타사항", "만기 후 이자율"];

const isExpandableField = (title) => {
  return expandableFields.includes(title);
};

onMounted(async () => {
  const id = route.params.id;
  try {
    product.value = await productStore.getProductDetail(id);
    reviews.value = await productStore.getReviews(id);
    userStore.loadUser();
    productInfo.value = {
      공시제출월: product.value.dcls_month,
      금융회사번호: product.value.fin_co_no,
      금융상품코드: product.value.fin_prdt_cd,
      유형: product.value.type,
      가입방법: product.value.join_way,
      가입제한: product.value.join_deny,
      가입대상: product.value.join_member,
      특별조건: product.value.spcl_cnd,
      기타사항: product.value.etc_note,
      "만기 후 이자율": product.value.mtrt_int,
      최대한도:
        product.value.max_limit !== null
          ? `${product.value.max_limit}원`
          : "없음",
      공시시작일: product.value.dcls_strt_day,
      공시종료일: product.value.dcls_end_day
        ? product.value.dcls_end_day
        : "없음",
      공시제출일: product.value.fin_co_subm_day,
    };
  } catch (error) {
    console.error("Failed to load product details:", error);
  }
});

const createReview = async () => {
  const id = route.params.id;
  const payload = {
    content: comment.value,
    deposit_product: id,
  };
  await productStore.createReview(id, payload);
  comment.value = "";
  reviews.value = await productStore.getReviews(id); // 댓글 목록을 새로고침
};

const deleteReview = async (reviewId) => {
  const id = route.params.id;
  await productStore.deleteReview(id, reviewId);
  reviews.value = await productStore.getReviews(id); // 댓글 목록을 새로고침
};

const toggleProduct = async (productId) => {
  await userStore.toggleProduct(productId);
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

h1,
h2,
.v-card-title,
.v-list-item-title {
  color: #5a3e36;
  font-family: "JG";
}

.v-card-subtitle,
.v-list-item-subtitle,
.wrap-text,
.expanded-subtitle {
  color: #5a3e36;
  font-family: "LGB";
}

.join-btn,
.submit-btn {
  background-color: #faf3dd;
  color: #000000;
  border-radius: 8px;
}

.v-container {
  margin-top: 20px;
}

.v-card {
  padding: 20px;
}

.mb-4 {
  margin-bottom: 20px;
}

.wrap-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}

.option-card {
  margin-bottom: 20px;
}

.expanded-subtitle {
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
  max-height: none; /* 최대 높이를 해제하여 텍스트가 완전히 보이도록 합니다 */
  display: block;
}
</style>
