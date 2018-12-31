from django.shortcuts import render, redirect
from django.views.generic import View


class MainPageView(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            user = request.user
            if user is not None and user.is_active:
                return render(request, "main/index.html", {})
        return redirect('login/')
