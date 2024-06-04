from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('stocklist/', views.stock_list),
    path('<str:ticker>/', views.stock_detail),
    path('<str:ticker>/plot/', views.stock_plot),
]