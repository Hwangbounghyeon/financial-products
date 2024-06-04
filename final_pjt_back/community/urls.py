from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('postlist/', views.post_list),
    path('create/', views.community_create),
    path('<int:pk>/', views.community),
    path('<int:pk>/comment/', views.comment),
    path('<int:pk>/comment/<int:comment_pk>/', views.modify_comment),
]