# encoding: utf-8
import csv
import re
import os
import subprocess
from  time import sleep


from emulador import instalar_apk, abrir_app, desinstalar_apk, ler_apks, abrir_emulator
from tela import capturar_tela, comparar_imagens



def main():

    caminho_original = '../apks/original/'
    apks = ['TippyTipper-debug', 'TranslateActivity-debug', 'arXiv-debug', 'ListLentObjects-debug']
    apps = ['net.mandaria.tippytipper', 'com.beust.android.translate', 'com.commonsware.android.arXiv', 'de.freewarepoint.whohasmystuff']
    activities = ['/.activities.TippyTipper', '/.TranslateActivity', '/.arXiv', '/.ListLentObjects']

    for i in range(len(apps)):
        apk = caminho_original + apks[i] + '.apk'
        instalar_apk(apk)
        saida = abrir_app(apps[i] + activities[i])

        if saida == 0:
            subprocess.call(
                ["timeout", "1h", "adb", "shell", "monkey", "--throttle", "200", "-p", apps[i], "-s", "1000",
                 "-v", "10", "--ignore-crashes", "--ignore-timeouts"])
            sleep(1)
            capturar_tela(apps[i] + '-original.png')
            sleep(0.2)
        else:
            print 'erro ao abrir app original: ' + apps[i]
            desinstalar_apk(apps[i])
            #exit(0)
        desinstalar_apk(apps[i])

    #3. executar casos de teste nos mutantes
    caminho_mutantes = '../apks/mutantes/'
    pastas_mutantes = ['tippytipper', 'translate', 'arxiv', 'whohasmystuff'] ### ATENCAO: deve estar na mesma ordem do vetor apps

    cont = 0

    for pasta in pastas_mutantes:
        resultado = []
        erros = 0
        apks = ler_apks(caminho_mutantes + pasta)
        # apks = ['TippyTipper-debug3.apk']

        for i in range(len(apks)):
            apk = caminho_mutantes + pasta + '/' + apks[i]
            instalar_apk(apk)

            saida = abrir_app(apps[cont] + activities[cont])
            match = re.search(r'\/[\w.-]+-debug\d+.apk', apk)
            fig_mutante = match.group()[1:-4] + '.png'

            if saida == 0:
                subprocess.call(
                    ["timeout", "1h", "adb", "shell", "monkey", "--throttle", "200", "-p", apps[cont], "-s", "1000",
                     "-v", "10", "--ignore-crashes", "--ignore-timeouts"])
                sleep(1)
                capturar_tela(fig_mutante)
                sleep(0.2)
                similar = comparar_imagens(apps[cont] + '-original.png', fig_mutante)
                resultado.append([apk, similar])
            else:
                erros += 1
                print 'erro ao abrir app mutante: ' + fig_mutante
                desinstalar_apk(apps[cont])


            desinstalar_apk(apps[cont])


        #4. resultados
        dm = 0
        tm = len(resultado)
        for r in resultado:
            print r
            if not r[1]:
                dm += 1


        print '------------------------ RESULTADOS ------------------------'
        print resultado
        m = 0
        if tm > 0:
            m = float(dm)/float(tm)
            print 'taxa de mutacao: ' + str(float(dm)/float(tm))
        else:
            print '[==> ATENÇÃO]: Total de mutantes válidos: 0'

        print 'erros: ' + str(erros)

        nome = 'resultado' + apps[cont]+'.csv'

        with open(nome, mode='w') as arquivo:
            arquivo = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            arquivo.writerow([resultado])
            arquivo.writerow([tm, m, erros])
        cont += 1




if __name__ == '__main__':
    main()
