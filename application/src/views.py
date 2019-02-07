from django.contrib.auth import logout
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from application.models import Checkpoint, Plate
from application.src.forms import CheckpointForm, PlateForm, AuthorizationForm


class CheckpointView(View):

    @staticmethod
    def get(request):
        form = CheckpointForm()

        if request.user.is_authenticated:
            user = request.user
            try:
                checkpoint = Checkpoint.objects.get(user=user)
            # check if checkpoint is created
            except ObjectDoesNotExist:
                return render(request, "main/creation.html", {'form': form})
            # check if checkpoint is created
            if user is not None and user.is_active:
                return render(request, "main/main.html", {'checkpoint': checkpoint})
        return redirect('login/')


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


class StreamView(View):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        from checkpoint.wsgi import camera
        self.camera = camera

    def gen(self):
        import time
        while True:
            time.sleep(0.2)
            buf = self.camera.buf

            if buf is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buf) + b'\r\n\r\n')
            return None

    @staticmethod
    def get(request):
        try:
            stream_view = StreamView()
            if stream_view.camera.buf is not None:
                return StreamingHttpResponse(
                    stream_view.gen(),
                    status=206,
                    content_type="multipart/x-mixed-replace;boundary=frame")
        finally:
            return HttpResponseServerError()


class UserAuthorizationView(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            return redirect('/')
        form = AuthorizationForm()
        return render(request, "authorization/login.html", {'form': form})

    @staticmethod
    def logout(request):
        logout(request)
        return redirect('/login')
