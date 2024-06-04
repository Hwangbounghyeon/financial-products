import json
import random
from collections import OrderedDict
from faker import Faker
from datetime import datetime

fake = Faker('ko-KR')

file = OrderedDict()

username_list = []
N = 100


# 저장 위치는 프로젝트 구조에 맞게 수정합니다.
save_dir = 'make_data/product_comment_data.json'
with open(save_dir, 'w', encoding="utf-8") as f:
    f.write('[')

    for i in range(N):
        # 랜덤한 데이터를 삽입
        file['model'] = 'products.ProductComment'
        file['pk'] = i + 1
        file['fields'] = {
            'user': random.randint(1, 100),  # 유저 이름 랜덤 생성
            # # 랜덤한 0~5개의 상품을 가입하도록 삽입됨
            # 'financial_products': ','.join(
            #     [
            #         random.choice(financial_products)
            #         for _ in range(random.randint(0, 5))
            #     ]
            # ),  # 금융 상품 리스트
            'deposit_product': random.randint(1, 101), 
            'content': fake.catch_phrase(),
            'created_at': datetime.fromisoformat(fake.date_time_this_year().isoformat()).strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.fromisoformat(fake.date_time_this_year().isoformat()).strftime('%Y-%m-%d %H:%M:%S'),
            'like': 0,
        }

        json.dump(file, f, ensure_ascii=False, indent='\t')
        if i != N - 1:
            f.write(',')
    f.write(']')
    f.close()
    
print(f'데이터 생성 완료 / 저장 위치: {save_dir}')