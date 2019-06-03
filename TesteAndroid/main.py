# encoding: utf-8
import csv
import re

from emulador import instalar_apk, abrir_app, desinstalar_apk, ler_apks
from tela import capturar_tela, comparar_imagens
from testador import executar_evento


def main():

    # 1. ler log (stoat e monkey)
    f = open('logs/teste.txt', 'r')
    # f = open('logs/mcmc_all_history_testsuites.txt', 'r')

    f1 = f.readlines()


    #2. executar casos de teste no programa original
    caminho_original = 'apks/original/'
    apks = ['TippyTipper-debug', 'TranslateActivity-debug', 'arXiv-debug', 'ListLentObjects-debug']
    apps = ['net.mandaria.tippytipper', 'com.beust.android.translate', 'com.commonsware.android.arXiv', 'de.freewarepoint.whohasmystuff']
    activities = ['/.activities.TippyTipper', '/.TranslateActivity', '/.arXiv', '/.ListLentObjects']
    #activities = ['/.activities.TippyTipper', '/TranslateActivity', '/arXiv', '/.activities.TippyTipper']
    # apks = ['TippyTipper-debug']
    # apps = ['net.mandaria.tippytipper']

    for i in range(len(apks)):
        apk = caminho_original + apks[i] + '.apk'
        instalar_apk(apk)
        saida = abrir_app(apps[i] + activities[i])
        if saida == 0:
            for l in f1:
                executar_evento(l)
            capturar_tela(apps[i] + '-original.png')
        else:
            print 'erro ao abrir app original: ' + apps[i]
            desinstalar_apk(apps[i])
            exit(0)
        desinstalar_apk(apps[i])

    #3. executar casos de teste nos mutantes
    caminho_mutantes = 'apks/mutantes/'
    pastas_mutantes = ['tippytipper', 'translate', 'arxiv', 'whohasmystuff'] ### ATENCAO: deve estar na mesma ordem do vetor apps

    for pasta in pastas_mutantes:
        resultado = []
        erros = 0
        apks = ler_apks(caminho_mutantes + pasta)
        # apks = ['TippyTipper-debug3.apk']
        for i in range(len(apks)):
            apk = caminho_mutantes + pasta + '/' + apks[i]
            instalar_apk(apk)
            # print apps[i] + '/.activities.TippyTipper'
            saida = abrir_app(apps[i] + activities[i]) #SplitBill
            match = re.search(r'\/[\w.-]+-debug\d+.apk', apk)
            fig_mutante = match.group()[1:-4] + '.png'
            # print fig_mutante

            if saida == 0:
                for l in f1:
                    executar_evento(l)

                capturar_tela(fig_mutante)
                similar = comparar_imagens(apps[i] + '-original.png', fig_mutante)
                resultado.append([apk, similar])
            else:
                erros += 1
                print 'erro ao abrir app mutante: ' + fig_mutante
                # desinstalar_apk(apps[i])
                # exit(0)

            desinstalar_apk(apps[i])



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

        with open('resultado.csv', mode='w') as arquivo:
            employee_writer = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            employee_writer.writerow([resultado])
            employee_writer.writerow([tm, m, erros])




if __name__ == '__main__':
    main()
