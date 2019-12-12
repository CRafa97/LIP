from django.urls import path
from lipApp import views

urlpatterns = [
    path('', views.index),
    path('load/', views.upload, name='load'),
    path('lac/<str:op>/', views.vlac, name='lac'),
    path('lmc/<str:op>/', views.vlmc, name='lmc')
]