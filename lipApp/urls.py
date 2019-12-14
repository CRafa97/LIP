from django.urls import path
from lipApp import views

urlpatterns = [
    path('', views.index),
    path('load/', views.upload, name='load'),
    path('load/select/<str:fldname>', views.select, name='select'),
    path('contrast/<str:op>/', views.contrast_ops, name='contrast'),
]