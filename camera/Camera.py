import time

import cv2


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.buf = None
        self.file_path = 'application/static/image/img.png'

        import threading
        t = threading.Thread(target=self.stream, args=())
        t.start()

    def stream(self):
        while True:
            try:
                time.sleep(0.1)
                if self.cap is not None:
                    ret, self.frame = self.cap.read()
                    if self.frame:
                        r, self.buf = cv2.imencode(".jpg", self.frame)
                        cv2.imwrite(self.file_path, self.frame)
            finally:
                pass
