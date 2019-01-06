import cv2


class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.buf = None
        import threading
        t = threading.Thread(target=self.stream, args=())
        t.start()

    def stream(self):
        if self.cap is not None:
            ret, self.frame = self.cap.read()
            r, self.buf = cv2.imencode(".jpg", self.frame)
        self.stream()
