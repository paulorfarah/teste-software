# -*- coding: utf-8 -*-
import csv
import logging
import re

from emulador import instalar_apk, abrir_app, desinstalar_apk, ler_apks
from tela import capturar_tela, comparar_imagens


class Tool(object):

    def __init__(self, pasta):
        self.__pasta = 'resultados/' + pasta + '/'

    def execute(self, tool, apps):
        caminho_base = 'apks/'
        for app in apps:
            cont = 0  # falta fazer loop e calcular a media
            # original
            apk_original = (caminho_base + 'original/' + app[0] + '.apk').strip()
            log = 'logs/' + app[3] + '/mcmc_all_history_testsuites_' + str(cont) + '.txt'
            erro1 = instalar_apk(apk_original)
            if erro1:
                # forçar desinstalacao de apps
                desinstalar_apk(app[1])
                erro1 = instalar_apk(apk_original)

            erro2 = abrir_app(app[1] + app[2])
            fig_original = app[3] + '-original.png'
            if not erro2:
                tool.execute([log, app[1]])
                capturar_tela(self.__pasta + 'telas/', app[3] + '-original.png')
            else:
                if erro1:
                    logging.error('[==> ATENÇÃO ]: Erro ao instalar app original: ' + app[3])
                elif erro2:
                    logging.error('[==> ATENÇÃO ]: Erro ao abrir app original: ' + app[3])
                else:
                    logging.error('[==> ATENCAO]: Erro desconhecido no app original ' + app[3])
                desinstalar_apk(app[1])
                exit(0)
            desinstalar_apk(app[1])

            ### MUTANTES
            resultado = []
            erros = 0
            apks = ler_apks(caminho_base + 'mutantes/' + app[3])
            # apks = ['TippyTipper-debug3.apk']
            for i in range(len(apks)):
                #instalar apk
                apk_mutante = caminho_base + 'mutantes/' + app[3] + '/' + apks[i]
                logging.info(apk_mutante)
                erro1 = instalar_apk(apk_mutante)

                #abrir app
                #print 'abrir app ' + app[1] + app[2]
                erro2 = abrir_app(app[1] + app[2])  # SplitBill
                if not erro1 and not erro2:
                    tool.execute([log, app[1]])

                    #capturar figura
                    match = re.search(r'\/[\w.-]+-debug\d+.apk', apk_mutante)
                    fig_mutante = match.group()[1:-4] + '.png'
                    # print fig_mutante
                    capturar_tela(self.__pasta + 'telas/', fig_mutante)

                    #comparar mutante com original
                    similar = comparar_imagens(self.__pasta + 'telas/', fig_original, fig_mutante)
                    resultado.append([app[3], similar])
                    logging.info(fig_original + ', ' + fig_mutante + ', ' + str(similar))
                else:
                    erros += 1
                    if erro1:
                        logging.error('[==> ATENÇÃO ]: Erro ao instalar app original: ' + apk_mutante)
                    elif erro2:
                        logging.error('[==> ATENÇÃO ]: Erro ao abrir app original: ' + app[1] + app[2])
                    else:
                        logging.error('[==> ATENCAO]: Erro desconhecido no app original ' + apk_mutante)
                desinstalar_apk(app[1])

            # 4. resultados
            dm = 0
            tm = len(resultado)
            for r in resultado:
                # print r
                if not r[1]:
                    dm += 1

            print '------------------------ RESULTADOS ------------------------'
            logging.info(str(resultado))
            m = 0
            if tm > 0:
                m = float(dm) / float(tm)
                print 'taxa de mutacao: ' + str(float(dm) / float(tm))
            else:
                print '[==> ATENÇÃO]: Total de mutantes válidos: 0'
            print 'erros: ' + str(erros)

            with open(self.__pasta + 'resultado.csv', mode='w') as arquivo:
                arquivo = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

                arquivo.writerow([resultado])
                arquivo.writerow(['total de mutantes', 'score de mutacao', 'erros'])
                arquivo.writerow([tm, m, erros])
            # media.append()
