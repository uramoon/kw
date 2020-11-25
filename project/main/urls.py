from django.urls import path

from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('loginform/', views.loginform, name='loginform'),
    path('join/', views.join, name='join'),
    path('register/', views.register, name='register'),
    path('testing/', views.testing, name='testing'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('welcome/', views.welcome, name='welcome'),
]