"""myApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from users import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='home', permanent=False)),  # 重定向到登录页面
    path('home/', views.home_view, name='home'),       # 登录页面
    path('HomeInterface/', views.homeInterface_view ,name='homeInterface'),
    path('login/', views.login_view, name='login'),       # 登录页面
    path('register/', views.register_view, name='register'), # 注册页面
    path('logout/', views.logout_view, name='logout'),     # 注销页面
    path('api/profile', views.user_profile, name='user_profile'),
    path('api/friends', views.user_friends, name='user_friends'),
    path('api/neighbors', views.user_friends, name='user_neighbors'),
    path('user/<int:user_id>/', views.user_details, name='user_detail'),
    path('api/hoods', views.user_hoods, name='hoods'),
    path('api/threads/hood/<int:hood_id>/', views.threads_in_hood, name='initial_messages_in_hood'),
    path('api/messages/thread/<int:thread_id>/', views.messages_in_thread, name='messages_in_thread'),
    path('api/messages/thread/<int:thread_id>/reply', views.reply_to_message, name='reply_to_message'),
    path("markers/", include("markers.urls"),),
    path('api/blocks', views.user_blocks, name='blocks'),
    path('api/threads/block/<int:block_id>/', views.threads_in_block, name='threads_in_block'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
