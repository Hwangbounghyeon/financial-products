import { api, authApi } from "@/api/index";

// 유저 정보를 삭제하는 함수
const dropOutApi = async (user) => {
  return authApi({
    method: "POST",
    url: "/accounts/dropout/",
    data: user,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

// 유저 프로필을 가져오는 함수
const profileApi = async (user) => {
  return authApi({
    method: "POST",
    url: `/accounts/${user.id}/`,
    data: user,
  })
    .then((response) => {
      console.log(response);
      return response;
    })
    .catch((error) => {
      console.log(error);
    });
};

export { dropOutApi, profileApi };
