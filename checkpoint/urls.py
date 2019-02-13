"""checkpoint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from application.src.controllers import *
from application.src.views import *

urlpatterns = [
    path('', CheckpointView.as_view(), name='main'),
    path('plate/', PlateView.as_view(), name='plate'),
    path('login/', UserAuthorizationView.as_view(), name='login'),
    path('logout/', UserAuthorizationView.logout, name='logout'),
    path('stream/', StreamView.as_view(), name='stream'),

    path('api/user/', UserController.as_view()),
    path('api/user/<str:token>/', UserController.as_view()),

    path('api/checkpoint/<str:token>/', CheckpointController.as_view()),
    path('api/checkpoint/<str:token>/<str:checkpoint>/', CheckpointController.as_view()),
    path('api/checkpoint/<str:token>/<str:checkpoint>/<int:active>/', CheckpointController.as_view()),

    path('admin/', admin.site.urls),
]
