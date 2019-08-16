from django.urls import path

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token 
from . import views


urlpatterns = [
    path('', views.WhichMoviePageView, name='home'),
    path('init/', views.WhichMovieInitView.as_view(), name='init'),
    path('message/', views.WhichMovieMessageView.as_view(), name='message'),
	path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]