import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";

export const useExchangeStore = defineStore("exchangeRate", () => {
  // 바로 화면 전환을 위한 router
  const router = useRouter();

  // 변수 선언
  const country = ref([]); // 환율 변경 선택 가능한 나라 리스트 저장
  const code = ref([]); // 환율 변경 나라와 매칭할 코드 리스트 저장
  const exchange = ref({}); // 나라이름: 통화코드의 정보를 저장
  const fromCountry = ref("대한민국"); // 변경되어 출력될 기준 통화로 하고 싶은 통화
  const toCountry = ref("미국"); // 변경하고 싶은 양을 입력할 통화 to: USD, from: KRW이면, 달러를 원화로 나타내고 싶다.
  const exchangeRateBase = ref(null); // 각국의 통화 코드를 key로 갖는 환율 객체가 저장될 변수
  const convertedMoney = ref(null); // 환율을 계산한 결과값을 저장하기 위한 변수
  const Money = ref(null); // 내가 입력한 돈을 저장할 변수
  const isSwap = ref(false); // swap을 체크할 변수. false면 convertedMoney 출력, treu면 tempMoney 출력.
  const tempConvertedMoney = ref(null); // swap시 계산된 결과를 바꾸기 위해 사용할 변수
  const icon = ref({}); // 국기 아이콘 리스트 저장

  // 환율 정보를 옵션으로 주기 위한 통화 코드 리스트를 불러오는 함수.
  const fetchCountryList = () => {
    axios({
      method: "get",
      url: "/datas/exchangeCountry.json",
    })
      .then((response) => {
        console.log(response.data);
        // country.value = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchCodeList = function () {
    axios({
      method: "GET",
      url: "/datas/exchangeCode.json",
    })
      .then((response) => {
        code.value = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchExchange = function () {
    axios({
      method: "GET",
      url: "/datas/exchange.json",
    })
      .then((response) => {
        exchange.value = response.data;
        // console.log(exchange.value);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchCountryIcons = function () {
    axios({
      method: "GET",
      url: "/datas/countryIcon.json",
    })
      .then((response) => {
        icon.value = response.data;
        console.log(icon.value);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // 환율 정보를 가져오는 함수
  const getExchangeRate = function () {
    console.log(icon.value);
    isSwap.value = false;
    axios({
      method: "GET",
      url: `https://v6.exchangerate-api.com/v6/${
        import.meta.env.VITE_APP_EXCHANGE_KEY
      }/latest/${exchange.value[toCountry.value]}`,
    })
      .then((response) => {
        // console.log(response.data.conversion_rates);
        exchangeRateBase.value = response.data.conversion_rates;

        for (const key in exchangeRateBase.value) {
          // 내가 입력한 값(Money.value)가 100이면,
          // 100 USD -> KRW => convertedMoney.value
          // 100 KRW -> USD => tempConvertedMoney.value

          // 만약 현재 key 값이 내가 입력한 fromCountry.value와 같다면
          if (key === exchange.value[fromCountry.value]) {
            // convertedMoeny와 tempConvertedMoney의 값을 계산한다.
            convertedMoney.value = (
              Money.value * exchangeRateBase.value[key]
            ).toFixed(4);
            tempConvertedMoney.value = (
              Money.value / exchangeRateBase.value[key]
            ).toFixed(4);
          }
        }
        // router.push({ name: "exchange-rate" });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // 바꾸기를 했을 때 나라이름을 바꾸고, 바뀌었는지 확인하기 위한 함수.
  const swapCountry = function () {
    const tempCountry = fromCountry.value;
    fromCountry.value = toCountry.value;
    toCountry.value = tempCountry;
    isSwap.value = !isSwap.value;
  };

  return {
    country,
    fromCountry,
    toCountry,
    exchangeRateBase,
    convertedMoney,
    Money,
    tempConvertedMoney,
    isSwap,
    exchange,
    code,
    icon,
    getExchangeRate,
    swapCountry,
    fetchCodeList,
    fetchCountryList,
    fetchExchange,
    fetchCountryIcons,
  };
});
