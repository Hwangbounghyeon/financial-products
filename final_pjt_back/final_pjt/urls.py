"""
URL configuration for final_pjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 로그인, 로그아웃, 비밀번호 변경 등의 기능을 제공
    path('accounts/', include('dj_rest_auth.urls')),
    # 회원가입, 이메일 인증, 소셜 로그인 등의 기능을 제공
    # path('account/signup/', include('dj_rest_auth.registration.urls')),
    # path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('community/', include('community.urls')),
    path('products/', include('products.urls')),
    path('stock/', include('stock.urls')),
    path('chatbot/', include('chatbot.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
