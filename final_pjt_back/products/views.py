from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DepositProduct,ProductComment,ProductCommentReport,Options
from .serializers import DepositProductSerializer, ProductCommentSerializer, ProductCommentReportSerializer, DepositProductDetailSerializer

# Create your views here.
@api_view(['GET'])
def product_list(request):
  if request.method == 'GET':
    products = DepositProduct.objects.all()
    serializer = DepositProductDetailSerializer(products, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def product_detail(request, pk):
  if request.method == 'GET':
    products = DepositProduct.objects.get(pk=pk)
    serializer = DepositProductDetailSerializer(products)
    return Response(serializer.data, status=200)
  
@api_view(['GET','POST'])
def product_review(request, pk):
  if request.method == 'GET':
    reviews = ProductComment.objects.filter(deposit_product=pk)
    serializer = ProductCommentSerializer(reviews, many=True)
    return Response(serializer.data)
  
  elif request.method == 'POST':
    serializer = ProductCommentSerializer(data = request.data)
    
    if serializer.is_valid(raise_exception=True):
      user = request.user
      serializer.save(user=user)
      return Response(serializer.data, status=201)

@api_view(['GET','PATCH','DELETE'])
def modify_review(request, pk, review_pk):
  if request.method == 'GET':
    review = ProductComment.objects.get(pk=review_pk)
    serializer = ProductCommentSerializer(review)
    return Response(serializer.data)
  
  elif request.method == 'PATCH':
    review = ProductComment.objects.get(pk=review_pk)
    serializer = ProductCommentSerializer(instance=review, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)

  elif request.method == 'DELETE':
    review = ProductComment.objects.get(pk=review_pk)
    review.delete()
    return Response(status=204)