import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import MainView from '@/views/MainView.vue';
import MapView from '@/views/MapView.vue';
import PostListView from '@/views/PostListView.vue';
import PostDetailView from '@/views/PostDetailView.vue';
import PostCreateView from '@/views/PostCreateView.vue';
import PostUpdateView from '@/views/PostUpdateView.vue';
import ProductListView from '@/views/ProductListView.vue';
import ProductDetailView from '@/views/ProductDetailView.vue';
import StockListView from '@/views/StockListView.vue';
import StockDetailView from '@/views/StockDetailView.vue';
import UesrProfileView from '@/views/UesrProfileView.vue';
import LogInView from '@/views/LogInView.vue';
import SignUpView from '@/views/SignUpView.vue';
import ExchangeView from '@/views/ExchangeView.vue';
import RecommendView from '@/views/RecommendView.vue';
import UpdateUserView from '@/views/UpdateUserView.vue';
import SubscribeProductView from '@/views/SubscribeProductView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'LogIn',
      component: LogInView,
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: SignUpView,
    },
    {
      path: '/',
      name: 'Main',
      component: MainView,
    },
    {
      path: '/map',
      name: 'Map',
      component: MapView,
    },
    {
      path: '/products',
      name: 'ProductList',
      component: ProductListView,
    },
    {
      path: '/products/:id',
      name: 'ProductDetail',
      component: ProductDetailView,
    },
    {
      path: '/posts',
      name: 'PostList',
      component: PostListView,
    },
    {
      path: '/posts/:id',
      name: 'PostDetail',
      component: PostDetailView,
    },
    {
      path: '/posts/:id/update',
      name: 'PostDetailUpdate',
      component: PostUpdateView,
    },
    {
      path: '/posts/create',
      name: 'PostCreateView',
      component: PostCreateView,
    },
    {
      path: '/stocks',
      name: 'StockList',
      component: StockListView,
    },
    {
      path: '/stocks/:ticker',
      name: 'StockDetail',
      component: StockDetailView,
    },
    {
      path: '/profile/:username',
      name: 'Profile',
      component: UesrProfileView,
    },
    {
      path: '/updateuser/:pk',
      name: 'UpdateUser',
      component: UpdateUserView,
    },
    {
      path: '/exchange',
      name: 'Exchange',
      component: ExchangeView,
    },
    {
      path: '/recommend',
      name: 'Recommend',
      component: RecommendView,
    },
    {
      path: '/subproduct',
      name: 'SubscribeProduct',
      component: SubscribeProductView,
    },
  ],
});

/* 로그인이 필요한 페이지에 진입할 때 사용하기 위한
navigation guard

router.beforeEach((to, from) => {
    const store = useUserStore();
    if (to.name === 'CreateView' && !store.isLogin) {
      window.alert('로그인이 필요합니다.')
      return {name: 'LogInView'}
    }
  })
*/

export default router;
