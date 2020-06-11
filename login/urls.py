from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.login_view, name='login-url'),
    path('for/', views.forgot, name='forgot-url'),
    path('reg/', views.signup, name='register-url'),
    path('log/', views.log, name='logout-url'),
    path(r'^act/(?P<email>\w{0,50})/$', views.activate, name='activate-url'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]