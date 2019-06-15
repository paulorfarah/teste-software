#-*- coding: utf-8 -*-

import os
from time import sleep
from PIL import Image, ImageChops
import math
import subprocess

STATUS_BAR_CROP_HEIGHT = 80
SCREEN_CPATURE_DELAY = 0.2
DIFF_THRESHOLD = 10
CRASH_THRESHOLD = 1000
RMS_THRESHOLD = 1


def checkSimilarPictures(pic1, pic2, x_max=DIFF_THRESHOLD, y_max=DIFF_THRESHOLD):
    # print pic1, pic2
    image1 = Image.open(pic1).convert('L')
    image2 = Image.open(pic2).convert('L')

    diff = ImageChops.difference(image1, image2)
    box = diff.getbbox()
    if box is None:
        return True, False

    xdiff = abs(box[0] - box[2])
    ydiff = abs(box[1] - box[3])

    if (xdiff >= x_max and ydiff >= y_max):
        # print 'Box', xdiff, ydiff
        h = diff.histogram()
        sq = (v * (i ** 2) for i, v in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares / float(image1.size[0] * image1.size[1]))
        # print rms
        if rms > RMS_THRESHOLD:
            # print 'RMS', rms
            if (xdiff >= CRASH_THRESHOLD and ydiff >= CRASH_THRESHOLD):
                return False, True
            return False, False
    return True, False




def comparar_imagens(pasta, arquivo1, arquivo2):
    img1 = os.path.join(pasta, arquivo1)
    img2 = os.path.join(pasta, arquivo2)
    similar, crashed = checkSimilarPictures(img1, img2)
    return similar


def capturar_tela(pasta, arquivo):
    image_path = os.path.join(pasta, arquivo)
    device_path = '/sdcard/%s' % arquivo
    sleep(SCREEN_CPATURE_DELAY)
    comando = ['adb', 'shell', "screencap -p", device_path]
    subprocess.call(comando)
    comando = ['adb', 'pull', device_path, image_path]
    subprocess.call(comando)
    while not os.path.isfile(image_path):
        sleep(0.1)
    comando = ['adb', 'shell', 'rm', device_path]
    subprocess.call(comando)
    img = Image.open(image_path)
    w, h = img.size
    img.crop((0, STATUS_BAR_CROP_HEIGHT, w, h)).save(image_path)
    return image_path
