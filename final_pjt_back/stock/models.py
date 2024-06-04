from django.db import models

class StockList(models.Model):
    ticker = models.CharField(max_length=255, primary_key=True)  # 코스피 시장에 상장된 ticker
    ticker_name = models.CharField(max_length=255)
    
class Stock(models.Model):
    ticker = models.ForeignKey(StockList, on_delete=models.CASCADE, related_name='stock')  # 코스피 시장에 상장된 ticker
    date = models.DateField()  # 날짜(주말, 공휴일 제외)
    opening_price = models.IntegerField()  # 시작가
    highest_price = models.IntegerField()  # 최고가
    lowest_price = models.IntegerField()  # 최저가
    closing_price = models.IntegerField()  # 종료가격
    volume = models.IntegerField()  # 거래량
    fluctuation_rate = models.FloatField()  # 전일대비 등락률
