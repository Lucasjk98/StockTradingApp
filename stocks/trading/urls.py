from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns=[
    path('', views.home, name = "home"),
    path('portfolio', views.portfolio, name = "portfolio"),
    path('buySell', views.buySell, name = "buySell")
]