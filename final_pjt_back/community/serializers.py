from rest_framework import serializers
from .models import Community, Comment, CommunityReport, CommentReport
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class CommunitySerializer(serializers.ModelSerializer):
    
    user = UserSerializer( read_only=True)
    class Meta:
        model = Community
        fields = '__all__'

        
class CommunityDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    comments = CommentSerializer(many=True,read_only=True)
    class Meta:
        model = Community
        fields = '__all__'


class CommunityReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityReport
        fields = '__all__'

class CommentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReport
        fields = '__all__'