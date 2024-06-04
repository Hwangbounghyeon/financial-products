from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User, LikeProduct
from products.serializers import DepositProductSerializer

class LikeProductSerializer(serializers.ModelSerializer):
  depositproducts = DepositProductSerializer(many=True, read_only=True)
  
  class Meta:
    model = LikeProduct
    fields = '__all__'
    
class UserSerializer(serializers.ModelSerializer):
  like_products = LikeProductSerializer(many=True, read_only=True)

  class Meta:
    model = User
    fields = '__all__'
    
class CustomRegisterSerializer(RegisterSerializer):
    nick_name = serializers.CharField(max_length=255, required=False)
    financial_products = serializers.CharField(allow_blank=True, allow_null=True)
    age = serializers.IntegerField(required=False)
    money = serializers.IntegerField(required=False)
    salary = serializers.IntegerField(required=False)
    img = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nick_name'] = self.validated_data.get('nick_name', '')
        data['financial_products'] = self.validated_data.get('financial_products', '')
        data['age'] = self.validated_data.get('age', 0)
        data['money'] = self.validated_data.get('money', 0)
        data['salary'] = self.validated_data.get('salary', 0)
        data['img'] = self.validated_data.get('img', None)
        return data

    def save(self, request):
        user = super().save(request)
        user.nick_name = self.data.get('nick_name')
        user.financial_products = self.data.get('financial_products')
        user.age = self.data.get('age')
        user.money = self.data.get('money')
        user.salary = self.data.get('salary')
        img = self.context['request'].FILES.get('img')
        if img:
            user.img = img
        user.save()
        return user