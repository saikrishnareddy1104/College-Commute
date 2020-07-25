from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [  
     path('register',views.register, name='register'),
     path('login',views.login,name='login'),
     path('logout',views.logout,name='logout'),
     path('offride',views.offride,name='offride'),
     path('lookride',views.lookride,name='lookride'),
     path('yourrides',views.yourrides,name='yourrides'),
     path('deleteride/<int:id>/', views.deleteyourride,name='deleteyourride'),
     url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
     path('joinride/<int:id>/', views.join,name='join'),  
     path('cancelride/<int:id>/', views.cancel,name='cancel'),
     path('userprofile/<str:username>/', views.userprofile,name='userprofile'),
     
 ] 