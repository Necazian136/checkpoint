from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import View
from application.src.entity.forms import *


class UserAuthorizationView(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('/')
        form = AuthorizationForm()
        return render(request, "authorization/login.html", {'form': form})

    @staticmethod
    def post(request):
        form = AuthorizationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
        # TODO: сделать отправку запроса на главный сервер, с получением обновлений при неудачной авторизации
        return render(request, "authorization/login.html", {'form': AuthorizationForm(request.POST)})
