from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('productlist/', views.product_list),
    path('<int:pk>/', views.product_detail),
    path('<int:pk>/review/', views.product_review),
    path('<int:pk>/review/<int:review_pk>', views.modify_review),
]