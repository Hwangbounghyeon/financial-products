import { api, authApi } from "@/api/index";

// 게시글 목록을 호출하는 함수
const getPostsApi = async () => {
  return api({
    method: "GET",
    url: "/community/postlist/",
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((err) => {
      console.log(err);
    });
};

// 게시글을 작성하는 함수
const createPostApi = async (post) => {
  return authApi({
    method: "POST",
    url: "/community/create/",
    data: {
      title: post.title,
      content: post.content,
    },
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 게시글의 상세 페이지를 호출하는 함수
const getPostDetailApi = async (post) => {
  return api({
    method: "GET",
    url: `/community/${post.id}/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 게시글을 수정하는 함수
const updatePostApi = async (post) => {
  return authApi({
    method: "PATCH",
    url: `/community/${post.id}/`,
    data: {
      title: post.title,
      content: post.content,
    },
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 게시글을 삭제하는 함수
const deletePostApi = async (post) => {
  return authApi({
    method: "DELETE",
    url: `/community/${post.id}/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 댓글을 작성하는 함수
const createCommentApi = async (post) => {
  return authApi({
    method: "POST",
    url: `/community/${post.id}/comment/`,
    data: {
      post: post.id,
      content: post.content,
    },
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 댓글을 가져오는 함수
const getCommentsApi = async (post) => {
  return api({
    method: "GET",
    url: `/community/${post.id}/comment/`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 댓글을 수정하는 함수
const updateCommentApi = async (post, comment) => {
  return authApi({
    method: "PATCH",
    url: `/community/${post.id}/comments/${comment.id}`,
    data: {
      post: post.id,
      content: post.content,
    },
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 댓글을 삭제하는 함수
const deleteCommentApi = async (post, comment) => {
  return authApi({
    method: "DELETE",
    url: `/community/${post.id}/comments/${comment.id}`,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

export {
  getPostsApi,
  createPostApi,
  getPostDetailApi,
  updatePostApi,
  deletePostApi,
  createCommentApi,
  getCommentsApi,
  updateCommentApi,
  deleteCommentApi,
};
