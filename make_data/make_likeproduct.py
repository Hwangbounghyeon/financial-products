import json
import random
from django.core.exceptions import ValidationError

# Load user and product data
user_file_path = 'make_data/user_data.json'
product_file_path = 'make_data/product_data.json'

with open(user_file_path, 'r', encoding='utf-8') as user_file:
    user_data = json.load(user_file)

with open(product_file_path, 'r', encoding='utf-8') as product_file:
    product_data = json.load(product_file)

# Parse users and sort by 'money'
users = sorted(user_data, key=lambda x: x['fields']['money'], reverse=True)

# Define product recommendation criteria based on user's money
high_net_worth_products = ['NH올원e예금', '토스뱅크 먼저 이자 받는 정기예금', '코드K 정기예금']
mid_net_worth_products = ['BNK더조은정기예금', 'Sh해양플라스틱Zero!예금', 'BNK주거래우대정기예금']
low_net_worth_products = ['하나의정기예금', '쏠편한 정기예금', '제주Dream정기예금']

product_mapping = {
    'high': high_net_worth_products,
    'mid': mid_net_worth_products,
    'low': low_net_worth_products
}

# Assign rating values
rating_values = {
    'high': 5.0,
    'mid': 4.0,
    'low': 3.0
}

# Determine product recommendation category based on user's money
def get_recommendation_category(money):
    if money >= 100000000:
        return 'high'
    elif money >= 50000000:
        return 'mid'
    else:
        return 'low'

# Create LikeProduct instances for each user based on their financial situation
like_products = []

pk_counter = 1  # Primary key counter for LikeProduct

while len(like_products) < 100:
    user = random.choice(users)
    user_money = user['fields']['money']
    recommendation_category = get_recommendation_category(user_money)
    recommended_products = product_mapping[recommendation_category]
    rating = rating_values[recommendation_category]

    product_name = random.choice(recommended_products)
    product = next((prod for prod in product_data if prod['fields']['fin_prdt_nm'] == product_name), None)
    
    if product:
        like_product = {
            'model': 'accounts.LikeProduct',
            'pk': pk_counter,
            'fields': {
                'user': user['pk'],
                'depositproduct': product['pk'],
                'rating': rating
            }
        }
        like_products.append(like_product)
        pk_counter += 1

# Save the LikeProduct data to a JSON file
like_product_file_path = 'make_data/like_product_data.json'
with open(like_product_file_path, 'w', encoding='utf-8') as like_product_file:
    json.dump(like_products, like_product_file, ensure_ascii=False, indent=4)

print(f'LikeProduct data saved to {like_product_file_path}')
