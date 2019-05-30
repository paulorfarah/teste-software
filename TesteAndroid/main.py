import os
from time import sleep
from PIL import Image
import subprocess
from image_checker import checkSimilarPictures

STATUS_BAR_CROP_HEIGHT = 80
SCREEN_CPATURE_DELAY = 0.2
SCREENSHOTS_DIRECTORY = 'D:\\PycharmProjects\\TesteAndroid\\telas\\'


def comparar_imagens(arquivo1, arquivo2):
    img1 = os.path.join(SCREENSHOTS_DIRECTORY, arquivo1)
    img2 = os.path.join(SCREENSHOTS_DIRECTORY, arquivo2)
    similar, crashed = checkSimilarPictures(img1, img2)
    return similar


def capturar_tela(pic_name, path):
    image_path = os.path.join(path, pic_name)
    device_path = '/sdcard/%s' % pic_name
    sleep(SCREEN_CPATURE_DELAY)
    command = ['adb', 'shell', "screencap -p", device_path]
    subprocess.call(command)
    command = ['adb', 'pull', device_path, image_path]
    subprocess.call(command)

    while not os.path.isfile(image_path):
        sleep(0.1)

    command = ['adb', 'shell', 'rm', device_path]
    subprocess.call(command)
    img = Image.open(image_path)
    w, h = img.size
    img.crop((0, STATUS_BAR_CROP_HEIGHT, w, h)).save(image_path)
    return image_path

def main():
    raw_input("Pressione ENTER para tirar a primeira foto...")
    capturar_tela('pic_name1.png', SCREENSHOTS_DIRECTORY)
    raw_input("Pressione ENTER para tirar a segunda foto...")
    capturar_tela('pic_name2.png', SCREENSHOTS_DIRECTORY)
    similar = comparar_imagens('pic_name1.png', 'pic_name2.png')
    if similar:
        print 'Imagens iguais'
    else:
        print 'Imagens diferentes'

if __name__ == '__main__':
    main()