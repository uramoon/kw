from django.urls import path
from django.conf.urls import url

from . import views
app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:nav_id>/', views.nav, name='nav'),

    path('subject/<str:code>', views.subject, name='subject'),
    path('subject/<str:code>/<int:post_id>', views.subpost, name='subpost'),
    path('subwrite/<str:code>/', views.subwrite, name='subwrite'),

    path('board/<int:board_id>/', views.board, name='board'),
    path('board/<int:board_id>/<int:post_id>', views.post, name='post'),
    path('write/<int:board_id>/', views.write, name='write'),       
    
    path('auth/loginform/', views.loginform, name='loginform'),
    path('auth/join/', views.join, name='join'),
    path('auth/register/', views.register, name='register'),
    path('auth/login/',views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/welcome/', views.welcome, name='welcome'),
]