import time
import cv2
from application.src.managers import KitLicensePlateManager, HistoryManager
from camera import recognition
import threading
from checkpoint.settings import BASE_DIR
# import RPi.GPIO as GPIO


class Camera:
    def __init__(self):
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(7, GPIO.OUT)
        self.kit_manager = KitLicensePlateManager()
        self.history_manager = HistoryManager()
        self.cap = cv2.VideoCapture(0)
        self.delay = 15
        self.frame = None
        self.buf = None
        self.file_path = 'application/static/images/camera_view.png'
        self.is_active = False
        self.__in_stream = False
        self.restart()

    def restart(self):
        if not (self.is_active or self.__in_stream):
            self.cap = cv2.VideoCapture(0)
            t = threading.Thread(target=self.stream, args=())
            t.start()
            if self.is_active:
                return True
        return False

    def stream(self):
        self.__in_stream = True
        while True:
            try:
                time.sleep(0.1)
                if self.cap is not None:
                    ret, self.frame = self.cap.read()
                    if self.frame is not None:
                        if not self.is_active:
                            self.is_active = True
                        r, self.buf = cv2.imencode(".jpg", self.frame)
                        cv2.imwrite(self.file_path, self.frame)
                        if self.recognize():
                            self.open_gate()
                    else:
                        self.is_active = False
                        break
            except Exception:
                self.is_active = False
        self.__in_stream = False


    def get_image_not_found(self):
        file = open(BASE_DIR + '/application/static/images/image-not-found.png', 'rb')
        bytes = file.read()
        file.close()
        return bytes

    def recognize(self):
        kits = self.kit_manager.get_active_kits()
        recognized_plates = recognition.recognize(self.file_path)
        for kit in kits:
            for plate in kit.plates:
                if plate in recognized_plates:
                    self.history_manager.add(plate, True)
                    return True
        return False

    def open_gate(self):
        #GPIO.output(7, True)
        time.sleep(self.delay)
        #GPIO.output(7, False)

    def __del__(self):
        pass
        # GPIO.cleanup()
