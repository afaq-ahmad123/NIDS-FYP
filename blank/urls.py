from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='404-url'),
    path('blank/', views.blank, name='blank-url'),
]