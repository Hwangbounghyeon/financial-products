from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('dropout/', views.dropout),
    path('<int:pk>/', views.profile), 
    path('recommend/', views.recommend),
    path('register/', views.CustomRegisterView.as_view(), name='custom_register'),
    path('user/', views.user_profile),
    path('toggle-financial-product/<int:pk>/', views.toggle_financial_product),
    path('<int:pk>/signupproduct/', views.signupproduct),
    path('<int:pk>/plots/', views.plots),
]