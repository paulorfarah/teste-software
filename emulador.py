import os
import subprocess

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
    #adb install -s example.apk
    print 'adb install -s ' + apk
    subprocess.call(["adb", "install", apk])

def desinstalar_apk(apk):
    print 'desinstalar apk'
    subprocess.call(["adb", "uninstall", apk])


def abrir_app(app):
    print 'abrir app'
    #adb shell am start -n com.package.name/com.package.name.ActivityName
    output = subprocess.call(["adb", "shell", "am", "start", "-n", app])
    print '---------------- output ---------------------------------'
    print output
    print '---------------- output ---------------------------------'
    return output


