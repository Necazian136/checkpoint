import cv2 as cv
from PIL import Image, ImageDraw
import numpy as np
import math


def show_image(img):
    cv.imshow('img', img)  # show input image with green boxes drawn around found digits
    cv.waitKey(0)


def resize(path, area=None, new_path=None):
    if not area:
        area = (336, 90)
    if not new_path:
        new_path = path
    image = cv.imread(path)
    resize_image = cv.resize(image, (area[0], area[1]))
    cv.imwrite(new_path, resize_image)


def make_grayscale(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray_image


def transform(image, area):
    area_array = sort_plate(area)
    rows, cols, ch = image.shape
    pts1 = np.float32([area_array[0], area_array[1], area_array[2]])
    pts2 = np.float32([[0, 0], [0, 90], [336, 0]])
    M = cv.getAffineTransform(pts1, pts2)
    dst = cv.warpAffine(image, M, (cols, rows))
    return dst


def sort_plate(area):
    area_array = []
    for a in area:
        area_array.append(a)
    area_array.sort(key=lambda coord: coord[0])
    if area_array[0][1] > area_array[1][1]:
        g = area_array[0][1]
        area_array[0][1] = area_array[1][1]
        area_array[1][1] = g
    if area_array[2][1] > area_array[3][1]:
        g = area_array[2][1]
        area_array[2][1] = area_array[3][1]
        area_array[3][1] = g
    return area_array[0], area_array[1], area_array[2], area_array[3]


def crop_image(im, area):
    crop_img = im[area[1]:area[3], area[0]:area[2]]
    return crop_img


def make_black_n_white(image, factor):
    image = make_grayscale(image)
    (thresh, im_bw) = cv.threshold(image, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    thresh = factor
    return cv.threshold(image, thresh, 255, cv.THRESH_BINARY)[1]


def make_negative(path, new_path=None):
    if not new_path:
        new_path = path
    image = Image.open(path)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    for i in range(width):
        for j in range(height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            draw.point((i, j), (255 - a, 255 - b, 255 - c))
    image.save(new_path, "JPEG")


def check_plate(box, conditions=None):
    try:
        min_size = conditions[0]
    except IndexError:
        min_size = (0, 0)
    try:
        max_size = conditions[1]
    except IndexError:
        max_size = (40000, 40000)
    try:
        ang = conditions[3]
    except IndexError:
        ang = 180

    width = max(box, key=lambda x: x[0])[0] - min(box, key=lambda x: x[0])[0]
    height = max(box, key=lambda x: x[1])[1] - min(box, key=lambda x: x[1])[1]
    edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
    edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

    # выясняем какой вектор больше
    usedEdge = edge1
    if cv.norm(edge2) > cv.norm(edge1):
        usedEdge = edge2
    reference = (1, 0)  # горизонтальный вектор, задающий горизонт

    # вычисляем угол между самой длинной стороной прямоугольника и горизонтом
    angle = int(180.0 / math.pi * math.acos(
        (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge))))
    if (min_size[0] < width < max_size[0]
        and min_size[1] < height < max_size[1]) \
            and (180 - ang < angle or ang > angle):
        return True
    return False


def find_plates(path):
    import subprocess, os, re, sys
    import json
    from .openalpr.src.bindings.python.build.lib.openalpr.openalpr import Alpr
    alpr = Alpr("eu",
                os.path.dirname(__file__) + "/openalpr/config/openalpr.conf.defaults",
                os.path.dirname(__file__) + "/openalpr/runtime_data")

    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

    alpr.set_top_n(10)
    alpr.set_default_region("md")

    results = alpr.recognize_file(path)['results']
    plates = []
    for result in results:
        coordinates = []
        for c in result['coordinates']:
            coordinates.append([c['x'], c['y']])
        plates.append(coordinates)
    return plates


def enlarge_box(box, size):
    left = size[0]
    up = size[1]
    right = size[2]
    down = size[3]
    box[0][0] -= left
    box[0][1] -= up
    box[1][0] -= left
    box[1][1] += down
    box[2][0] += right
    box[2][1] -= up
    box[3][0] += right
    box[3][1] += down
    return box


def sort_boxes(boxes):
    boxes.sort(key=lambda box: int(((box[1][0] - box[0][0]) ** 2 + (box[1][1] - box[0][1]) ** 2) ** 0.5 *
                                   ((box[2][0] - box[0][0]) ** 2 + (box[2][1] - box[0][1]) ** 2) ** 0.5))
    return boxes