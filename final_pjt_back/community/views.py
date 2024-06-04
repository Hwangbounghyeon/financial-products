from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Community,Comment,CommunityReport,CommentReport
from .serializers import CommentSerializer,CommunitySerializer,CommunityReportSerializer,CommentReportSerializer,CommunityDetailSerializer

# Create your views here.
@api_view(['GET'])
def post_list(request):
  if request.method == 'GET':
    communitys = Community.objects.all()
    serializer = CommunitySerializer(communitys, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def community_create(request):
  if request.method == 'POST':
    serializer = CommunitySerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
      user = request.user
      serializer.save(user=user)
      return Response(serializer.data, status=201)

@api_view(['GET', 'PUT', 'DELETE'])
def community(request, pk):
    try:
        community = Community.objects.get(pk=pk)
    except Community.DoesNotExist:
        return Response({'error': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommunityDetailSerializer(community)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if community.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommunityDetailSerializer(community, data=request.data, partial=True)
        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if community.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def comment(request,pk):
  if request.method == 'GET':
    comment = Comment.objects.filter(community=pk)
    serializer = CommentSerializer(comment, many=True)
    return Response(serializer.data)
  elif request.method == 'POST':
    serializer = CommentSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
      user = request.user
      serializer.save(user=user)
      return Response(serializer.data, status=201)

@api_view(['PUT', 'DELETE'])
def modify_comment(request, pk, comment_pk):
  if request.method == 'PUT':
    review = Comment.objects.get(pk=comment_pk)
    serializer = CommentSerializer(instance=review, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      return Response(serializer.data)

  elif request.method == 'DELETE':
    review = Comment.objects.get(pk=comment_pk)
    review.delete()
    return Response(status=204)
    