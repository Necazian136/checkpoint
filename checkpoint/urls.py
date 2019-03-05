"""kit URL Configuration

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
from django.urls import path, re_path
from django.views.generic import RedirectView

from application.src.controllers import *
from application.src.views import *

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('kit/', KitView.as_view(), name='kit'),
    path('kit/<str:kit>/', PlateView.as_view(), name='plate'),
    path('login/', UserAuthorizationView.as_view(), name='login'),
    path('logout/', UserAuthorizationView.logout, name='logout'),
    path('stream/', StreamView.as_view(), name='stream'),

    path('api/user/', UserController.as_view()),

    path('api/kit/', KitController.as_view()),
    path('api/kit/<str:kit>/', KitController.as_view()),
    path('api/kit/<str:kit>/<int:active>/', KitController.as_view()),

    path('api/plate/<str:kit>/', PlateController.as_view()),
    path('api/plate/<str:kit>/<str:plate>/', PlateController.as_view()),

    path('admin/', admin.site.urls),  # TODO: закоментировать когда сервер будет готов

    re_path('/+$', RedirectView.as_view(pattern_name='main', permanent=False)),
]
