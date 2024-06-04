import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import { useUserStore } from '@/stores/userStore';
import { useRouter } from 'vue-router';
import axios from 'axios';

export const useComStore = defineStore(
  'community',
  () => {
    const userStore = useUserStore();
    const router = useRouter();
    const posts = ref([]);
    const comments = ref([]);
    const BASE_URL = 'http://localhost:8000/community';

    // 게시글 목록 가져오는 함수
    const getPosts = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/postlist/`);
        posts.value = response.data;
      } catch (error) {
        console.error('Failed to fetch posts:', error);
      }
    };

    // 게시글 상세 정보 가져오는 함수
    const getPostDetail = async (id) => {
      try {
        const response = await axios.get(`${BASE_URL}/${id}/`);
        return response.data;
      } catch (error) {
        console.error('Failed to fetch post detail:', error);
      }
    };

    // 게시글 검색하는 함수
    const searchPost = (query) => {
      return posts.value.filter((post) =>
        post.title.toLowerCase().includes(query.toLowerCase())
      );
    };

    // 게시글 작성하는 함수
    const createPost = async (postData) => {
      try {
        const response = await axios.post(`${BASE_URL}/create/`, postData, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        posts.value.push(response.data);
        router.push({ name: 'PostList' });
      } catch (error) {
        console.error('Failed to create post:', error);
      }
    };

    // 게시글 수정하는 함수
    const updatePost = async (id, postData) => {
      try {
        const response = await axios.put(`${BASE_URL}/${id}/`, postData, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        const index = posts.value.findIndex((post) => post.id === id);
        if (index !== -1) {
          posts.value[index] = response.data;
        }
        router.push({ name: 'PostDetail', params: { id: id } });
      } catch (error) {
        console.error('Failed to update post:', error);
      }
    };

    // 게시글 삭제하는 함수
    const deletePost = async (id) => {
      try {
        await axios.delete(`${BASE_URL}/${id}/`, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        posts.value = posts.value.filter((post) => post.id !== id);
      } catch (error) {
        console.error('Failed to delete post:', error);
      }
    };

    // 게시글 좋아요 누르는 함수
    const likePost = async (id) => {
      try {
        const response = await axios.post(`${BASE_URL}/${id}/like/`);
        const index = posts.value.findIndex((post) => post.id === id);
        if (index !== -1) {
          posts.value[index].likes = response.data.likes;
        }
      } catch (error) {
        console.error('Failed to like post:', error);
      }
    };

    // 댓글 목록 가져오는 함수
    const getComments = async (postId) => {
      try {
        const response = await axios.get(`${BASE_URL}/${postId}/comment/`);
        comments.value = response.data;
      } catch (error) {
        console.error('Failed to fetch comments:', error);
      }
    };

    // 댓글 작성하는 함수
    const createComment = async (postId, commentData) => {
      try {
        const response = await axios.post(
          `${BASE_URL}/${postId}/comment/`,
          commentData,
          {
            headers: {
              Authorization: `Token ${userStore.token}`,
            },
          }
        );
        comments.value.push(response.data);
      } catch (error) {
        console.error('Failed to create comment:', error);
      }
    };

    // 댓글 수정하는 함수
    const updateComment = async (postId, commentId, commentData) => {
      try {
        const response = await axios.put(
          `${BASE_URL}/${postId}/comment/${commentId}/`,
          commentData
        );
        const index = comments.value.findIndex(
          (comment) => comment.id === commentId
        );
        if (index !== -1) {
          comments.value[index] = response.data;
        }
      } catch (error) {
        console.error('Failed to update comment:', error);
      }
    };

    // 댓글 삭제하는 함수
    const deleteComment = async (postId, commentId) => {
      try {
        await axios.delete(`${BASE_URL}/${postId}/comment/${commentId}/`, {
          headers: {
            Authorization: `Token ${userStore.token}`,
          },
        });
        comments.value = comments.value.filter(
          (comment) => comment.id !== commentId
        );
      } catch (error) {
        console.error('Failed to delete comment:', error);
      }
    };

    return {
      posts,
      comments,
      getPosts,
      getPostDetail,
      searchPost,
      createPost,
      updatePost,
      deletePost,
      likePost,
      createComment,
      getComments,
      updateComment,
      deleteComment,
    };
  },
  { persist: true }
);
