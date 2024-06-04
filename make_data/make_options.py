# make_data.py 파일은 랜덤한 더미 데이터를 만드는 예시 파일입니다.
# 반드시, 사용하는 필드를 확인한 후 본인의 프로젝트에 맞게 수정하여 진행해야 합니다.

# [참고] 현재 코드는 아래 User 모델을 기준으로 작성되어 있습니다.
"""
class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    money = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    # 가입한 상품 목록 리스트를 ,로 구분된 문자열로 저장함
    financial_products = models.TextField(blank=True, null=True)

    # superuser fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
"""


import requests



# 현재 API 에 들어있는 금융 상품 코드 리스트 저장
DP_URL = 'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json'
SP_URL = 'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json'

API_KEY = ''

financial_products = []

params = {
    'auth': API_KEY,
    # 금융회사 코드 020000(은행), 030200(여신전문), 030300(저축은행), 050000(보험), 060000(금융투자)
    'topFinGrpNo': '020000',
    'pageNo': 1,
}

# 정기예금 목록 저장
response = requests.get(DP_URL, params=params).json()
baseList = response.get('result').get('optionList')  # 상품 목록

pk = 1

for options in baseList:
    options_list = {
    'model': 'products.Options',
    'pk': pk,
    'fields': {
        'deposit_product': 1,
        'dcls_month': options['dcls_month'],
        'fin_co_no': options['fin_co_no'],
        'fin_prdt_cd': options['fin_prdt_cd'],
        'intr_rate_type': options['intr_rate_type'],
        'intr_rate_type_nm': options['intr_rate_type_nm'],
        'save_trm': options['save_trm'],
        'intr_rate': options['intr_rate'],
        'intr_rate2': options['intr_rate2']
    }
}
    pk += 1 
    financial_products.append(options_list)

# 적금 목록 저장
response = requests.get(SP_URL, params=params).json()
baseList = response.get('result').get('optionList')  # 상품 목록

for options in baseList:
    options_list = {
    'model': 'products.Options',
    'pk': pk,
    'fields': {
        'deposit_product': 1,
        'dcls_month': options['dcls_month'],
        'fin_co_no': options['fin_co_no'],
        'fin_prdt_cd': options['fin_prdt_cd'],
        'intr_rate_type': options['intr_rate_type'],
        'intr_rate_type_nm': options['intr_rate_type_nm'],
        'save_trm': options['save_trm'],
        'intr_rate': options['intr_rate'],
        'intr_rate2': options['intr_rate2']
    }
}

    pk += 1
    financial_products.append(options_list)

import json

# 이전에 생성한 DepositProduct JSON 데이터 불러오기
with open('make_data/product_data.json', 'r', encoding='utf-8') as file:
    deposit_products = json.load(file)

# 각 DepositProduct의 fin_prdt_cd와 일치하는 Options 데이터 찾아 deposit_product 필드에 넣기
for options in financial_products:
    for deposit_product in deposit_products:
        if options['fields']['fin_prdt_cd'] == deposit_product['fields']['fin_prdt_cd']:
            options['fields']['deposit_product'] = deposit_product['pk']
            break
        

# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = 'make_data/product_options_data.json'
with open(save_dir, 'w', encoding="utf-8") as f:
    json.dump(financial_products, f, ensure_ascii=False, indent=4)
    # f.write(str(financial_products))
    # f.close()

print(f'데이터 생성 완료 / 저장 위치: {save_dir}')

