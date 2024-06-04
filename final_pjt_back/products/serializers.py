from rest_framework import serializers
from .models import DepositProduct, ProductComment, ProductCommentReport, Options
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        


class ProductCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ProductComment
        fields = '__all__'
        

class ProductCommentReportSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    class Meta:
        model = ProductCommentReport
        fields = '__all__'
        
        
# class OptionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Options
#         fields = '__all__'

# class DepositProductDetailSerializer(serializers.ModelSerializer):
#     options_set = OptionsSerializer(many=True, read_only=True)

#     class Meta:
#         model = DepositProduct
#         fields = '__all__'

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['intr_rate_type', 'intr_rate_type_nm', 'save_trm', 'intr_rate', 'intr_rate2']
        
class DepositProductDetailSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True, read_only=True)

    class Meta:
        model = DepositProduct
        fields = '__all__'
        
class DepositProductSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True, read_only=True)
    class Meta:
        model = DepositProduct
        fields = '__all__'


