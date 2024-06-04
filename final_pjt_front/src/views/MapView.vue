<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-row align="center" justify="center" class="w-100">
      <v-col cols="12" md="10">
        <v-card class="pa-6 card-outline main-card">
          <v-card-title class="headline text-center">
            <h1>진짜 카카오 지도</h1>
          </v-card-title>
          <v-card-text>
            <div class="search-container">
              <div class="direct-search">
                <label style="font-family: 'LGB'" for="enter"
                  >직접 입력:
                </label>
                <input
                  v-model="directKeyword"
                  placeholder="검색어를 직접 입력하세요"
                  @keyup.enter="searchPlaces"
                />
                <button @click="searchPlaces">🔎</button>
              </div>
              <div class="dropdown-search">
                <label for="province">도 : </label>
                <select
                  id="province"
                  v-model="selectedProvince"
                  @change="onProvinceChange"
                >
                  <option value="" disabled>'도'를 선택하세요</option>
                  <option
                    v-for="province in provinces"
                    :key="province"
                    :value="province"
                  >
                    {{ province }}
                  </option>
                </select>
                <label for="city">시/군/구 : </label>
                <select
                  id="city"
                  v-model="selectedCity"
                  :disabled="!selectedProvince"
                  @change="onCityChange"
                >
                  <option value="" disabled>'시/군/구'를 선택하세요</option>
                  <option
                    v-for="city in cities[selectedProvince] || []"
                    :key="city"
                    :value="city"
                  >
                    {{ city }}
                  </option>
                </select>
                <label for="town">읍/면/동 : </label>
                <select
                  id="town"
                  v-model="selectedTown"
                  :disabled="!selectedCity"
                >
                  <option value="" disabled>'읍/면/동'을 선택하세요</option>
                  <option
                    v-for="town in towns[selectedProvince]?.[selectedCity] ||
                    []"
                    :key="town"
                    :value="town"
                  >
                    {{ town }}
                  </option>
                </select>
                <label for="bank">은행 : </label>
                <select
                  id="bank"
                  v-model="selectedBank"
                  :disabled="!selectedProvince"
                >
                  <option value="" disabled>'은행명'을 선택하세요</option>
                  <option v-for="bank in banks" :key="bank" :value="bank">
                    {{ bank }}
                  </option>
                </select>
                <button @click="searchPlaces">🔎</button>
                <button class="current-location-btn" @click="searchNearbyBanks">
                  현재 위치 기준으로 검색
                </button>
              </div>
            </div>
            <div id="map-container">
              <div id="map" class="map"></div>
              <div class="sidebar" :class="{ closed: sidebarClosed }">
                <h2 @click="toggleSidebar">검색 결과</h2>
                <ul v-if="places.length > 0">
                  <li
                    v-for="(place, index) in places"
                    :key="index"
                    :class="{ selected: selectedPlaceIndex === index }"
                    @click="clickSidebarItem(index)"
                  >
                    <strong>{{ place.place_name }}</strong
                    ><br />
                    주소: {{ place.address_name }}<br />
                    도로명주소: {{ place.road_address_name }}<br />
                    전화번호: {{ place.phone }}
                  </li>
                </ul>
              </div>
            </div>
            <div class="zoom-buttons">
              <button @click="zoomIn">+</button>
              <button @click="zoomOut">-</button>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const baseCoordinate = ref({ latitude: 0, longitude: 0 });
const coordinateError = ref("");

const banks = ref(null);
const provinces = ref([]);
const cities = ref({});
const towns = ref({});
const selectedProvince = ref("");
const selectedCity = ref("");
const selectedTown = ref("");
const selectedBank = ref("");
const places = ref([]);
const selectedPlaceIndex = ref(null);
const sidebarClosed = ref(false);

const getInfomations = async () => {
  axios({
    method: "get",
    url: "/datas/MapBankName.json",
  })
    .then((response) => {
      banks.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });

  axios({
    method: "get",
    url: "/datas/MapAddress.json",
  })
    .then((response) => {
      provinces.value = response.data.provinces;
      cities.value = response.data.cities;
      towns.value = response.data.towns;
    })
    .catch((error) => {
      console.log(error);
    });
};

const onProvinceChange = () => {
  selectedCity.value = "";
  selectedTown.value = "";
};

const onCityChange = () => {
  selectedTown.value = "";
};

const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        baseCoordinate.value.latitude = position.coords.latitude;
        baseCoordinate.value.longitude = position.coords.longitude;
        initializeMap();
      },
      (error) => {
        alert("좌표를 가져오는 과정에서 에러가 발생했습니다!");
        coordinateError.value = error.message;
        console.log(coordinateError.value);
      }
    );
  } else {
    alert("현재 좌표를 가져올 수 없습니다!");
  }
};

const directKeyword = ref("");
const map = ref(null);
const infowindow = ref(null);
const ps = ref(null);
const markers = ref([]);
const bigMarkers = ref(new Set());

const initializeMap = () => {
  const mapContainer = document.getElementById("map");
  const mapOption = {
    center: new kakao.maps.LatLng(
      baseCoordinate.value.latitude,
      baseCoordinate.value.longitude
    ),
    level: 3,
  };

  map.value = new kakao.maps.Map(mapContainer, mapOption);
  ps.value = new kakao.maps.services.Places();
  infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 });
};

onMounted(() => {
  getCurrentLocation();
  getInfomations();
});

const searchPlaces = function () {
  const optionKeyword = [
    selectedProvince.value,
    selectedCity.value,
    selectedTown.value,
    selectedBank.value,
  ].join("");

  if (!directKeyword.value.replace(/^\s+|\s+$/g, "") && !optionKeyword) {
    alert("검색어를 입력해 주세요!");
    return false;
  }

  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];

  selectedProvince.value = "";
  selectedCity.value = "";
  selectedTown.value = "";
  selectedBank.value = "";
  console.clear();

  if (optionKeyword) {
    ps.value.keywordSearch(optionKeyword, placesSearchCB);
  } else {
    ps.value.keywordSearch(directKeyword.value, placesSearchCB);
  }
};

function placesSearchCB(data, status, pagination) {
  if (status === kakao.maps.services.Status.OK) {
    places.value = data;
    const bounds = new kakao.maps.LatLngBounds();

    for (let i = 0; i < data.length; i++) {
      displayMarker(data[i], i);
      bounds.extend(new kakao.maps.LatLng(data[i].y, data[i].x));
    }

    map.value.setBounds(bounds);
  } else {
    alert("검색 결과가 없습니다.");
    resetSearch();
  }
}

function displayMarker(place, index) {
  const imageSize = new kakao.maps.Size(24, 35);
  const bigImageSize = new kakao.maps.Size(30, 44);

  const markerImage = new kakao.maps.MarkerImage(
    "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png",
    imageSize
  );
  const bigMarkerImage = new kakao.maps.MarkerImage(
    "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png",
    bigImageSize
  );

  const marker = new kakao.maps.Marker({
    map: map.value,
    position: new kakao.maps.LatLng(place.y, place.x),
    image: markerImage,
  });

  markers.value.push(marker);

  kakao.maps.event.addListener(marker, "click", function () {
    selectedPlaceIndex.value = index;
    map.value.panTo(new kakao.maps.LatLng(place.y, place.x));
    if (bigMarkers.value.has(marker)) {
      marker.setImage(markerImage);
      infowindow.value.close();
      bigMarkers.value.delete(marker);
    } else {
      marker.setImage(bigMarkerImage);
      infowindow.value.setContent(
        `<div style="padding:5px;font-size:12px;">
          <strong>${place.place_name}</strong><br />
          주소: ${place.address_name}<br />
          도로명주소: ${place.road_address_name}<br />
          전화번호: ${place.phone}
        </div>`
      );
      infowindow.value.open(map.value, marker);
      bigMarkers.value.add(marker);
    }
  });
}

const clickSidebarItem = (index) => {
  kakao.maps.event.trigger(markers.value[index], "click");
};

const resetSearch = () => {
  selectedProvince.value = "";
  selectedCity.value = "";
  selectedTown.value = "";
  selectedBank.value = "";
  directKeyword.value = "";
  places.value = [];
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];
  initializeMap();
};

const toggleSidebar = () => {
  sidebarClosed.value = !sidebarClosed.value;
};

const zoomIn = () => {
  const currentLevel = map.value.getLevel();
  map.value.setLevel(currentLevel - 1);
};

const zoomOut = () => {
  const currentLevel = map.value.getLevel();
  map.value.setLevel(currentLevel + 1);
};

const searchNearbyBanks = () => {
  const lat = baseCoordinate.value.latitude;
  const lng = baseCoordinate.value.longitude;
  const radius = 2000;

  const placesService = new kakao.maps.services.Places();
  const options = {
    location: new kakao.maps.LatLng(lat, lng),
    radius: radius,
    category_group_code: "BK9",
  };

  placesService.keywordSearch("은행", placesSearchCB, options);
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
  height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.card-outline {
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  width: 100%;
}

.main-card {
  padding: 20px;
  margin: 20px auto;
  max-width: 1200px;
  border-radius: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.headline {
  font-family: "JG";
  font-size: 24px;
  color: #5a3e36; /* 타이틀 폰트 색상 변경 */
  margin-bottom: 10px;
}

.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.direct-search {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.direct-search input {
  margin-right: 10px;
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: "LGB";
}

.direct-search button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  background-color: #a3d5ff; /* 버튼 배경색 변경 */
  color: white;
  cursor: pointer;
  font-family: "LGB";
}

.dropdown-search {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.dropdown-search label,
.dropdown-search select {
  margin-right: 10px;
  font-family: "LGB";
}

.dropdown-search select {
  padding: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: "LGB";
}

.dropdown-search button {
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  background-color: #a3d5ff; /* 버튼 배경색 변경 */
  color: white;
  cursor: pointer;
  font-family: "LGB";
}

.current-location-btn {
  padding: 10px;
  border: none;
  border-radius: 10px;
  background-color: #a3d5ff; /* 버튼 배경색 변경 */
  color: white;
  cursor: pointer;
  font-family: "LGB";
  margin-left: 10px;
}

#map-container {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

#map {
  width: 70%;
  height: 600px;
  border-radius: 15px;
  transition: border-radius 0.3s;
}

.map {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.sidebar {
  width: 25%;
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  background: rgba(255, 255, 255, 0.9);
  z-index: 1000;
  transition: transform 0.3s ease;
  border-radius: 15px;
}

.sidebar.closed {
  transform: translateX(300px);
}

.sidebar h2 {
  cursor: pointer;
  font-family: "LGB";
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  cursor: pointer;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 5px;
  font-family: "LGB";
}

.sidebar li:hover {
  background: rgba(240, 240, 240, 0.8);
}

.sidebar li.selected {
  background: rgba(200, 200, 255, 0.8);
}

.zoom-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.zoom-buttons button {
  width: 50px;
  height: 50px;
  font-size: 1.5rem;
  margin: 5px;
  border-radius: 50%;
  border: none;
  background-color: #a3d5ff; /* 버튼 배경색 변경 */
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s;
  font-family: "LGB";
}

.zoom-buttons button:hover {
  background-color: #84c0e8;
}
</style>
