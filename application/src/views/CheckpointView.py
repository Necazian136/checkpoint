from django.shortcuts import render, redirect
from django.views.generic import View

from application.models import Checkpoint, User
from application.src.forms.CheckpointForm import CheckpointForm


class CheckpointView(View):

    @staticmethod
    def get(request):
        form = CheckpointForm()

        if request.user.is_authenticated:
            user = request.user
            checkpoint = user.checkpoint
            if user is not None and user.is_active:
                return render(request, "main/index.html", {'form': form, 'checkpoint': checkpoint})
        return redirect('login/')

    @staticmethod
    def post(request):
        form = CheckpointForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            checkpoint_name = form.cleaned_data['name']

            # search user in database by request user
            user = User.objects.get(username=request.user.username)

            # TODO: Сделать отправку запроса на сервер для синхронизации
            # create checkpoint
            checkpoint = Checkpoint(name=checkpoint_name)
            checkpoint.save()

            # add checkpoint in user at database
            user.checkpoint = checkpoint
            user.save()

            # add checkpoint in user at request
            request.user.checkpoint = checkpoint
            request.user.save()

        return CheckpointView.get(request)
