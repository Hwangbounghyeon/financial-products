from rest_framework import serializers
from .models import Stock, StockList

        
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        
class StockListSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True, many=True)
    
    class Meta:
        model = StockList
        fields = '__all__'