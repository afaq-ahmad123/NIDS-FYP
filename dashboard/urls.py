# from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='dash-url'),
    path('run/', views.run, name='run-url'),
    # path('auto/', views.auto, name='auto-url'),
    # path('dnn/', views.dnn, name='dnn-url'),
    # path('lstm/', views.lstm, name='lstm-url'),
    # path('naive/', views.Naive, name='naive-url'),
    # path('cap/', views.packt_acquire, name='packt-url'),
]