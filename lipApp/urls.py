from django.urls import path
from lipApp import views

urlpatterns = [
    path('', views.index)
]