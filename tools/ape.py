#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Imports the monkeyrunner modules used by this program
# from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import os

from monkeyrun.base import MonkeyRunner

print("Iniciando Conexão com o Dispositivo")
# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
print("Dispositivo Conectado")




def executar_evento(linha, texto):
    x = 0
    y = 0
    cont = 0
    pula = 0
    lista_frente = None
    lista = linha.split(" ")
    print(lista)
    if pula == 0:
        if lista[2] == "touch":
            x_antigo = x
            y_antigo = y

            posicao = lista[5].split(",")

            x = int(round(float(posicao[0]), 0))
            y = int(round(float(posicao[1]), 0))

            if lista[3] == "ACTION_MOVE":
                try:
                    lista_frente = texto[cont + 1].split(" ")
                except Exception:
                    print("Fim de arquivo")
                if lista_frente[2] == "throttle":
                    tempo = float(lista_frente[3]) / 1000
                    device.drag((x_antigo, y_antigo), (x, y), tempo, 10)
                    pula = 1
            elif lista[3] == "ACTION_DOWN":
                try:
                    lista_frente = texto[cont + 1].split(" ")
                    lista_frente_2 = texto[cont + 2].split(" ")
                    lista_frente_7 = texto[cont + 7].split(" ")
                except Exception:
                    print("Fim de arquivo")
                if lista_frente[2] == "throttle":
                    device.drag((x, y), (x, y), 1, 10)
                    pula = 2
                elif (lista_frente[3] == "ACTION_MOVE") and (lista_frente_2[2] == "throttle"):
                    lista_frente_21 = texto[cont + 21].split(" ")
                    posicao_21 = lista_frente_21[5].split(",")
                    x_frente_21 = int(round(float(posicao_21[0]), 0))
                    y_frente_21 = int(round(float(posicao_21[1]), 0))
                    device.drag((x, y), (x_frente_21, y_frente_21), 1, 10)
                    pula = 21
                elif (lista_frente[3] == "ACTION_MOVE") and (lista_frente_2[3] == "ACTION_MOVE"):
                    achei = 0
                    contador = 0
                    while achei != 1:
                        contador = contador + 1
                        lista_frente_z = texto[cont + contador].split(" ")
                        if (lista_frente_z[3]) == "ACTION_UP":
                            achei = 1
                    posicao_z = lista_frente_z[5].split(",")
                    x_frente_z = int(round(float(posicao_z[0]), 0))
                    y_frente_z = int(round(float(posicao_z[1]), 0))
                    device.drag((x, y), (x_frente_z, y_frente_z), 0.1, contador - 1)
                    pula = contador
                elif (lista_frente[3] == "ACTION_MOVE") and (lista_frente_2[3] == "ACTION_UP"):
                    posicao_w = lista_frente_2[5].split(",")
                    x_frente_w = int(round(float(posicao_w[0]), 0))
                    y_frente_w = int(round(float(posicao_w[1]), 0))
                    device.drag((x, y), (x_frente_w, y_frente_w), 0.1, 1)
                    pula = 2
                else:
                    device.touch(float(posicao[0]), float(posicao[1]), "DOWN")
                    pula = 1
            elif lista[3] == "ACTION_UP":
                device.touch(float(posicao[0]), float(posicao[1]), "UP")


        elif lista[2] == "trackball":

            x_antigo = x
            y_antigo = y

            posicao = lista[5].split(",")

            # x = int(round(float(posicao[0]), 0))*200
            # y = int(round(float(posicao[1]), 0))*51
            x = int(round(float(posicao[0]), 0))
            y = int(round(float(posicao[1]), 0))

            if lista[3] == "ACTION_MOVE":

                # device.drag((x_antigo, y_antigo), (x_antigo + x, y_antigo + y), 0.3, 1)
                # device.touch(x_antigo + x, y_antigo + y, "UP")
                # device.touch(x_antigo + x, y_antigo + y, "UP")
                # MonkeyRunner.sleep(0.5)
                # device.touch(200, 770, "DOWN_AND_UP")
                # print(x_antigo)
                # print(x)
                # print(x_antigo + x)
                # print(y_antigo)
                # print(y)
                # print(y_antigo + y)
                x = x_antigo + x
                y = y_antigo + y
            elif lista[3] == "ACTION_UP":
                device.touch(x, y, "UP")
                x = x_antigo + x
                y = y_antigo + y
            elif lista[3] == "ACTION_DOWN":
                device.touch(x, y, "DOWN")
                x = x_antigo + x
                y = y_antigo + y


        elif lista[2] == "throttle":
            MonkeyRunner.sleep(float(lista[3]) / 1000)
            MonkeyRunner.sleep(float(lista[3]) / 1000)
            MonkeyRunner.sleep(float(lista[3]) / 1000)


        elif lista[2] == "start":
            device.shell('am start com.commonsware.android.arXiv/.arXiv')
            # device.shell('am start de.freewarepoint.whohasmystuff/.ListLentObjects')
            # device.shell('am start com.beust.android.translate/.TranslateActivity')
            # device.shell('am start net.mandaria.tippytipper/.activities.TippyTipper')


        elif lista[2] == "key_down":
            device.press(lista[4], MonkeyDevice.DOWN)
            # device.press(KEYCODE_DPAD_UP, MonkeyDevice.DOWN_AND_UP)
            MonkeyRunner.sleep(0.1)


        elif lista[2] == "key_up":
            device.press(lista[4], MonkeyDevice.UP)
            MonkeyRunner.sleep(0.1)


        elif lista[2] == "persist":
            os.system("adb shell settings put system accelerometer_rotation 1")
            if int(lista[3]) == 0:
                os.system("adb shell settings put system user_rotation 0")
            elif int(lista[3]) == 1:
                os.system("adb shell settings put system user_rotation 1")
            elif int(lista[3]) == 2:
                os.system("adb shell settings put system user_rotation 2")
            elif int(lista[3]) == 3:
                os.system("adb shell settings put system user_rotation 3")


        elif int(lista[2]) == 0:
            os.system("adb shell settings put system user_rotation 0")


        elif int(lista[2]) == 1:
            os.system("adb shell settings put system accelerometer_rotation 0")
            os.system("adb shell settings put system user_rotation 1")


        elif int(lista[2]) == 2:
            os.system("adb shell settings put system accelerometer_rotation 0")
            os.system("adb shell settings put system user_rotation 2")


        elif int(lista[2]) == 3:
            os.system("adb shell settings put system accelerometer_rotation 0")
            os.system("adb shell settings put system user_rotation 3")
    else:
        pula = pula - 1
    cont = cont + 1
class Ape(object):

    def execute(self, params):
        # print("Iniciando Leitura do Arquivo")
        # arq = open('/home/elton/PycharmProjects/testador/venv/consume.log', 'r')
        # texto = arq.readlines()
        # print("Término da Leitura do Arquivo")
        arq = open(params[0], 'r')
        texto = arq.readlines()
        for linha in texto:
            executar_evento(linha, texto)
        arq.close()



