from django.views.generic import View
from django.http import StreamingHttpResponse
import time


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

    @staticmethod
    def get(request):
        try:
            stream_view = StreamView()
            return StreamingHttpResponse(
                stream_view.gen(),
                status=206,
                content_type="multipart/x-mixed-replace;boundary=frame")
        finally:
            pass
