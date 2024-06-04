import json
import random
import os

# Load user and product data
user_file_path = 'make_data/user_data.json'
product_file_path = 'make_data/product_data.json'
like_product_file_path = 'make_data/like_product_data.json'

with open(user_file_path, 'r', encoding='utf-8') as user_file:
    user_data = json.load(user_file)

with open(product_file_path, 'r', encoding='utf-8') as product_file:
    product_data = json.load(product_file)

# Initialize like_product_data if the file does not exist
if os.path.exists(like_product_file_path):
    with open(like_product_file_path, 'r', encoding='utf-8') as like_product_file:
        like_product_data = json.load(like_product_file)
else:
    like_product_data = []

# Define financial product categories with at least 30 products each
high_net_worth_products = [20, 18, 21, 12, 16, 14, 15, 22, 24, 36, 30, 19]
mid_net_worth_products = [17, 3, 4, 5, 6, 7, 8, 9, 10, 11, 25, 26, 27, 28, 29]
low_net_worth_products = [1, 2, 13, 31, 32, 33, 34, 35]

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

# Function to determine recommendation category based on salary
def get_recommendation_category(salary):
    if salary >= 100000:
        return 'high'
    elif salary >= 50000:
        return 'mid'
    else:
        return 'low'

# Function to generate random value within a range with variation
def generate_value(base, variation):
    return random.randint(int(base * (1 - variation)), int(base * (1 + variation)))

# Function to generate user data
def generate_user_data(pk, username):
    # Randomly select age and salary to ensure diverse distribution
    age = random.randint(20, 70)
    salary = random.randint(2000, 200000)
    
    category = get_recommendation_category(salary)
    
    money = salary * random.randint(1, 12)  # Ensure money is a multiple of salary

    num_products = random.randint(2, 5)
    products = random.sample(product_mapping[category], num_products)

    user_data = {
        'model': 'accounts.User',
        'pk': pk,
        'fields': {
            'username': username,
            'financial_products': ','.join(map(str, products)),
            'age': age,
            'money': money,
            'salary': salary,
            'password': '1234',
            'nick_name': None,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
    }
    return user_data

# Function to generate user data with product type specific ranges
def generate_user_data_with_product_type(pk, username, products):
    if any(product in high_net_worth_products for product in products):
        age = generate_value(50, 0.5)  # Base 50, 50% variation
        money = generate_value(10000000 * 12, 0.5)  # Base 120,000,000, 50% variation
        salary = generate_value(10000000, 0.3)  # Base 10,000,000, 30% variation
    elif any(product in mid_net_worth_products for product in products):
        age = generate_value(35, 0.5)  # Base 35, 50% variation
        money = generate_value(4500000 * 12, 0.5)  # Base 54,000,000, 50% variation
        salary = generate_value(4500000, 0.3)  # Base 4,500,000, 30% variation
    else:
        age = generate_value(30, 0.3)  # Base 30, 30% variation
        money = generate_value(3000000 * 12, 0.5)  # Base 36,000,000, 50% variation
        salary = generate_value(3000000, 0.3)  # Base 3,000,000, 30% variation

    user_data = {
        'model': 'accounts.User',
        'pk': pk,
        'fields': {
            'username': username,
            'financial_products': ','.join(map(str, products)),
            'age': age,
            'money': money,
            'salary': salary,
            'password': '1234',
            'nick_name': None,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
        }
    }
    return user_data

# Generate user data with financial products and attributes
N = 100  # Number of users to generate
new_user_data = []

for i in range(N):
    user_pk = i + 1
    username = f'user{user_pk}'
    
    recommendation_category = get_recommendation_category(random.choice(range(0, 200000)))  # Random salary choice
    available_products = product_mapping[recommendation_category]
    num_products = random.randint(2, min(5, len(available_products)))
    recommended_products = random.sample(available_products, num_products)
    
    user_entry = generate_user_data_with_product_type(user_pk, username, recommended_products)
    new_user_data.append(user_entry)

# Save the new user data to a JSON file
save_dir = 'make_data/new_user_data.json'
with open(save_dir, 'w', encoding='utf-8') as f:
    json.dump(new_user_data, f, ensure_ascii=False, indent=4)

print(f'New user data saved to {save_dir}')

# Create LikeProduct instances only if the products are in financial_products
like_products = []
pk_counter = 1  # Primary key counter for LikeProduct

for like_product in like_product_data:
    user_id = like_product['fields']['user']
    product_id = like_product['fields']['depositproduct']

    # Find user and their financial products
    user = next((user for user in new_user_data if user['pk'] == user_id), None)
    if user and str(product_id) in user['fields']['financial_products'].split(','):
        category = get_recommendation_category(user['fields']['salary'])  # Add category determination
        like_product_entry = {
            'model': 'accounts.LikeProduct',
            'pk': pk_counter,
            'fields': {
                'user': user_id,
                'depositproduct': product_id,
                'rating': rating_values[category]
            }
        }
        like_products.append(like_product_entry)
        pk_counter += 1

# Save the LikeProduct data to a JSON file
new_like_product_file_path = 'make_data/new_like_product_data.json'
with open(new_like_product_file_path, 'w', encoding='utf-8') as like_product_file:
    json.dump(like_products, like_product_file, ensure_ascii=False, indent=4)

print(f'LikeProduct data saved to {new_like_product_file_path}')
