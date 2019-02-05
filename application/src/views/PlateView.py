from django.shortcuts import render, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from application.models import Checkpoint, Plate
from application.src.forms.PlateForm import PlateForm


class PlateView(View):

    @staticmethod
    def get(request):
        form = PlateForm()

        if request.user.is_authenticated:
            user = request.user
            try:
                checkpoint = Checkpoint.objects.get(user=user)
                plates = Plate.objects.filter(checkpoint=checkpoint)
            # check if checkpoint is created
            except ObjectDoesNotExist:
                return render(request, "main/creation.html", {'form': form})
            # check if user is authenticated
            if user is not None and user.is_active:
                return render(request, "plate/plate.html", {'form': form, 'plates': plates})
        return redirect('login/')

    @staticmethod
    def post(request):
        form = PlateForm(request.POST)

        if form.is_valid() and request.user.is_authenticated:
            plate_name = form.cleaned_data['name']

            try:
                checkpoint = Checkpoint.objects.get(user=request.user)
            # check if checkpoint is created
            except ObjectDoesNotExist:
                return render(request, "main/creation.html", {'form': form})
            # creating plate
            plate = Plate(number=plate_name, checkpoint=checkpoint)
            plate.save()
            # increase sync counter for synchronisation with server
            checkpoint.sync_counter += 1
            checkpoint.save()

        return PlateView.get(request)

    @staticmethod
    def delete(request):
        form = request.DELETE
        print(form)
