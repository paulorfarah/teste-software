#-*- coding: utf-8 -*-
import os
import subprocess
import sys


def ler_apks(basepath):
    # List all files in a directory using os.listdir
    # basepath = 'my_directory/'
    arquivos = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            # print(entry)
            arquivos.append(entry)
    return arquivos

def instalar_apk(apk):
    print 'instalar apk'
    comando = ["adb", "install", apk]
    output = subprocess.call(comando)
    return output

def desinstalar_apk(apk):
    print 'desinstalar apk'
    comando = ["adb", "uninstall", apk]
    subprocess.call(comando)


def abrir_app(app):
    print 'abrir app'
    comando = ["adb", "shell", "am", "start", "-n", app]
    output = 1
    msg = ''
    try:
        msg = subprocess.check_output(comando, stderr=subprocess.STDOUT)
        output = 0
        if 'Error type 3' in msg and 'Error: Activity class' in msg and 'does not exist.' in msg:
            output = 1
            # print msg
            # 'Starting: Intent { cmp=com.beust.android.translate/.TranslateActivity }
            # Error type 3
            # Error: Activity class {com.beust.android.translate / com.beust.android.translate.TranslateActivity} does not exist.
    except subprocess.CalledProcessError as e:
        # handle errors in the called executable
        print e.output
    except OSError:
        # executable not found
        print sys.exc_info()
    return output


