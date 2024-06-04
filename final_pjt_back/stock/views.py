from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StockList,Stock
from .serializers import StockSerializer, StockListSerializer

# Create your views here.
@api_view(['GET'])
def stock_list(request):
  if request.method == 'GET':
    stock_list = StockList.objects.all()
    serializer = StockListSerializer(stock_list,many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def stock_detail(request,ticker):
  if request.method == 'GET':
    stock = StockList.objects.filter(ticker=ticker)
    serializer = StockListSerializer(stock,many=True)
    return Response(serializer.data, status=200)
  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import StockList
from .serializers import StockListSerializer
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

@api_view(['GET'])
def stock_plot(request, ticker):
    if request.method == 'GET':
        stock_list = StockList.objects.filter(ticker=ticker)
        serializer = StockListSerializer(stock_list, many=True)

        if not stock_list:
            return Response({"error": "No stock data found for this ticker"}, status=404)
        
        # Prepare data for time series analysis
        stock_data = serializer.data[0]['stock']
        df = pd.DataFrame(stock_data)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Train ARIMA model for forecasting
        model = ARIMA(df['closing_price'], order=(5, 1, 0))
        model_fit = model.fit()

        # Forecast the next 3 days
        forecast = model_fit.forecast(steps=3)
        forecast_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=3)

        forecast_data = {
            'forecast_dates': forecast_dates.strftime('%Y-%m-%d').tolist(),
            'forecast_prices': forecast.tolist()
        }

        response_data = {
            'historical_data': stock_data,
            'forecast_data': forecast_data
        }


        return Response(response_data)
