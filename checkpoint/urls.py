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
from application.src.views.UserAuthorizationView import UserAuthorizationView
from application.src.views.CheckpointView import CheckpointView
from application.src.views.StreamView import StreamView
from application.src.views.PlateView import PlateView

urlpatterns = [
    path('', CheckpointView.as_view(), name='checkpoint'),
    path('plate/', PlateView.as_view(), name='plate'),
    path('login/', UserAuthorizationView.as_view(), name='auth'),
    path('stream/', StreamView.as_view(), name='stream'),
    path('admin/', admin.site.urls),
]
