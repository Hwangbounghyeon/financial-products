# Django관련 라이브러리
import os
import re
import json
import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import User, LikeProduct
from .serializers import UserSerializer, LikeProductSerializer
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer, UserSerializer
from products.models import DepositProduct
from products.serializers import DepositProductSerializer, DepositProductDetailSerializer


class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

@api_view(['GET'])
@authentication_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    return Response(user)

@api_view(['DELETE'])
@login_required
def dropout(request):
    request.user.delete()
    auth_logout(request)
    return Response(status=204)

@api_view(['GET','PUT'])
def profile(request, pk):
    if request.method == 'GET':
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
@api_view(['POST'])
@login_required
def toggle_financial_product(request,pk):
    user = request.user
    product_id = str(pk)

    if not product_id:
        return Response({'error': 'Product ID not provided'}, status=400)

    financial_products = user.financial_products.split(',') if user.financial_products else []

    if product_id in financial_products:
        financial_products.remove(product_id)
        action = '삭제'
    else:
        financial_products.append(product_id)
        action = '추가'

    user.financial_products = ','.join(financial_products)
    user.save()

    return JsonResponse({'action': action, 'financial_products': user.financial_products})

@api_view(['GET'])
def signupproduct(request, pk):
    user = get_object_or_404(User, pk=pk)
    product_ids = user.financial_products.split(',') if user.financial_products else []
    products = DepositProduct.objects.filter(id__in=product_ids)
    serializer = DepositProductSerializer(products, many=True)
    return Response(serializer.data)


# 유저의 정보를 받아와 유저에게 맞는 상품 추천
@api_view(['GET'])
@login_required
def recommend(request):
    user = request.user

    if not hasattr(user, 'salary') or not hasattr(user, 'age'):
        return Response({"error": "User does not have salary or age attribute"}, status=status.HTTP_400_BAD_REQUEST)

    user_salary = user.salary
    user_age = user.age

    # 클러스터링 결과 파일 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'clustering_results_3_clusters.csv')

    # 클러스터링 결과 불러오기
    df = pd.read_csv(file_path)

    # 클러스터를 salary_max와 age_max으로 정렬
    df_sorted = df.sort_values(by=['salary_max', 'age_max'])

    # 추천할 금융 상품 리스트
    recommended_products = []

    # 유저의 salary와 age를 비교하여 적절한 클러스터의 financial_products 추천
    for _, row in df_sorted.iterrows():
        # if row['salary_max'] > user_salary and row['age_max'] > user_age:
        if row['salary_max'] > user_salary:
            recommended_products = list(json.loads(row['financial_products'].replace("'", "\"")).keys())[:10]
            break

    # 만약 2번째로 큰 클러스터보다 salary와 age가 많다면 가장 큰 클러스터의 financial_products 추천
    second_largest_cluster = df_sorted.iloc[-2]
    largest_cluster = df_sorted.iloc[-1]
    # if user_salary > second_largest_cluster['salary_max'] and user_age > second_largest_cluster['age_max']:
    if user_salary > second_largest_cluster['salary_max']:
        recommended_products = list(json.loads(largest_cluster['financial_products'].replace("'", "\"")).keys())[:10]
    
    recommended_products_info = DepositProduct.objects.filter(pk__in=recommended_products).values()
    # serializer = DepositProductSerializer(recommended_products_info, many=True)

    return Response(recommended_products_info)

# 가입한 상품 금리 그래프
from django.http import HttpResponse
import pandas as pd
import numpy as np

@api_view(['GET'])
# @login_required
def plots(request, pk):
    user = get_object_or_404(User, pk=pk)
    product_ids = user.financial_products.split(',') if user.financial_products else []
    products = DepositProduct.objects.filter(id__in=product_ids)
    serializer = DepositProductDetailSerializer(products, many=True)
    
    # Convert serializer data to DataFrame
    products_df = pd.DataFrame(serializer.data)
    
    # Extract relevant rates from options
    def extract_rates(options):
        save_trm_12 = next((opt for opt in options if opt['save_trm'] == '12'), {})
        return {
            'intr_rate': save_trm_12.get('intr_rate', None),
            'intr_rate2': save_trm_12.get('intr_rate2', None)
        }
    
    products_df['intr_rate'] = products_df['options'].apply(lambda x: extract_rates(x)['intr_rate'])
    products_df['intr_rate2'] = products_df['options'].apply(lambda x: extract_rates(x)['intr_rate2'])
    
    # Keep only necessary columns
    products_df = products_df[['fin_prdt_nm', 'intr_rate', 'intr_rate2']]
    
    # Replace NaN and infinite values with 0 or any suitable value
    products_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    products_df.fillna(value=0, inplace=True)
    
    # Calculate average rates
    avg_intr_rate = products_df['intr_rate'].mean()
    avg_intr_rate2 = products_df['intr_rate2'].mean()
    
    # Add average rates to the DataFrame
    avg_row = pd.DataFrame([{
        'fin_prdt_nm': '평균 금리',
        'intr_rate': avg_intr_rate,
        'intr_rate2': avg_intr_rate2
    }])
    products_df = pd.concat([avg_row, products_df], ignore_index=True)
    
    # Convert DataFrame to JSON serializable format
    products_json = products_df.to_dict('records')
    
    return Response({"data": products_json})