"""Project1 URL Configuration

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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from MainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('social-auth/',include('social_django.urls',namespace='social_auth')),
    path("",views.home,name='home'),
    path('repos/',views.repos_list,name='repos_list'),
    path('create/',views.create_repo,name='repo_create'),
    path('get-repo/',views.get_repo,name="get_repo"),
    path('<str:repo_name>/delete/', views.delete_repo, name='repo_delete'),
         
]
