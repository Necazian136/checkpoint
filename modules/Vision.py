import cv2


class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.buf = None
        self.filepath = 'img.jpg'
        import threading
        t = threading.Thread(target=self.stream, args=())
        t.start()

    def stream(self):
        while True:
            if self.cap is not None:
                ret, self.frame = self.cap.read()
                r, self.buf = cv2.imencode(".jpg", self.frame)
                cv2.imwrite(self.filepath, self.frame)
