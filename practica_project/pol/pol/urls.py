"""
URL configuration for pol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from masterpol import views

urlpatterns = [ #маршрутизация, присваиваю так-же имена ччто-бы понятнее указывать путь в templates
    path('', views.show_partners, name = 'show_partners'),
    path('add/', views.add, name = 'add'),
    path('history/', views.history, name = 'history'),
    path('login/', views.login, name = 'login'),
    path('edit/', views.edit_partner, name='edit_partner'),
]
