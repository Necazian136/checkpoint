import cv2
import os

from .car_plate_recognition import cpr
from .russian_word_recognition import rwr


def recognize(file):
    plates = cpr.find_plates(file)
    # Распознавание символов на табличке
    variants = []
    for plate in plates:
        plate = cpr.sort_plate(plate)
        img = cv2.imread(file)
        tr = cpr.transform(img, plate)
        ci = cpr.crop_image(tr, (0, 0, 336, 90))
        recognized_number = rwr.recognize(ci)
        if recognized_number:
            predicted_number = rwr.predict_number(recognized_number)
            if predicted_number:
                variants.append(predicted_number)
            else:
                pl = cpr.enlarge_box(plate, (3, 3, 3, 3))
                tr = cpr.transform(img, pl)
                ci = cpr.crop_image(tr, (0, 0, 336, 90))
                for i in range(32, 224, 32):
                    img2 = cpr.make_black_n_white(ci, i)
                    cv2.imwrite('bw.jpg', img2)
                    img2 = cv2.imread('bw.jpg')
                    os.remove('bw.jpg')
                    recognized_number = rwr.recognize(img2)
                    if recognized_number:
                        predicted_number = rwr.predict_number(recognized_number)
                        if predicted_number:
                            variants.append(predicted_number)
    return sorted(variants, key=lambda x: -len(x))
