from django.contrib.auth import logout
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from application.src.managers import *
import time


class MainView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kit_manager = KitLicensePlateManager()
        self.history_manager = HistoryManager()

    def get(self, request):
        if request.user is not None and request.user.is_active:
            return render(request, "main/main.html", {'history': self.history_manager.get_all()})
        return redirect('/login/')


class KitView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()
        self.kit_manager = KitLicensePlateManager()

    def get(self, request):
        if request.user is not None and request.user.is_active:
            kit_list = self.kit_manager.get_kits(request.user)
            return render(request, "kit/kit.html", {'kit_list': kit_list})
        return redirect('/login/')


class PlateView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()
        self.kit_manager = KitLicensePlateManager()
        self.plate_manager = PlateManager()

    def get(self, request, **kwargs):
        try:
            if (request.user.is_authenticated and request.user is not None and request.user.is_active):
                user = request.user

                kit = None
                plates = None

                if 'kit' in kwargs:
                    kit = self.kit_manager.get_kit_by_name(kwargs['kit'], user)
                if kit is not None:
                    plates = self.plate_manager.get_plates(kit)
                if plates is not None:
                    return render(request, "plate/plate.html", {'kit': kit, 'plate_list': plates})
        except Exception:
            return redirect("/kit/")
        return redirect('/login/')


class StreamView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from checkpoint.wsgi import camera
        self.camera = camera

    def gen(self):
        while True:
            time.sleep(0.2)
            buf = self.camera.buf

            if buf is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + bytearray(buf) + b'\r\n\r\n')
            yield None

    def get(self, request):
        if request.user is not None and request.user.is_active:
            try:
                if self.camera.is_active or self.camera.restart():
                    return StreamingHttpResponse(self.gen(), status=206,
                                                 content_type="multipart/x-mixed-replace;boundary=frame")

            except Exception as e:
                pass
            return HttpResponse(self.camera.get_image_not_found(), content_type="image/jpeg")
        return redirect('/login')


class UserAuthorizationView(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_manager = UserManager()

    def get(self, request):
        if request.user is not None and request.user.is_active:
            return redirect('/')
        return render(request, "authorization/login.html")

    @staticmethod
    def logout(request):
        logout(request)
        return redirect('/login/')
