"""twitter_back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views
from user_app.views import LoginView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('user/', include('user_app.urls', namespace='user')),
    path('news/', include('news_app.urls', namespace='news')),
    path('api-auth/', include('rest_framework.urls')),
    path('api_auth_token/', views.obtain_auth_token, name='api_auth_token'),
    path('login/', LoginView.as_view(), name='login'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)