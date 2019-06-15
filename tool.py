# -*- coding: utf-8 -*-
import csv
import datetime
import logging
import re
import time

from emulador import instalar_apk, abrir_app, desinstalar_apk, ler_apks
from tela import capturar_tela, comparar_imagens

def ler_log_mutantes(log):
    op_mutantes = {}
    with open('logs/'+log, 'r') as f:
        for linha in f:
            if not linha.strip(): continue # skip the empty line
            l = linha.replace('ThreadPool: 1', '').split()
            op_mutantes[l[1][:-1]] = l[3]
    return op_mutantes


class Tool(object):

    def __init__(self, pasta):
        self.__pasta = 'resultados/' + pasta + '/'

    def execute(self, tool, apps):
        caminho_base = 'apks/'
        for app in apps:
            scores_mutacao = []
            with open(self.__pasta + 'resultado_' + app[3] + '.csv', mode='w') as arquivo:
                arquivo = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for cont in range(3, 6): # falta fazer loop e calcular a media

                    # ORIGINAL
                    ##############################################################################
                    apk_original = (caminho_base + 'original/' + app[0] + '.apk').strip()
                    log = 'logs/' + app[3] + '/mcmc_all_history_testsuites_' + str(cont) + '.txt'
                    erro1 = instalar_apk(apk_original)
                    if erro1:
                        # forçar desinstalacao de apps
                        desinstalar_apk(app[1])
                        erro1 = instalar_apk(apk_original)

                    erro2 = abrir_app(app[1] + app[2])
                    time.sleep(1)
                    fig_original_ini = app[3] + '-original-ini.png'
                    fig_original = app[3] + '-original.png'
                    if not erro2:
                        capturar_tela(self.__pasta + 'telas/', fig_original_ini)
                        tool.execute([log, app[1]])
                        capturar_tela(self.__pasta + 'telas/', fig_original)
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
                    ####################################################################
                    resultado = []
                    op_mutantes_total = {}
                    op_mutantes_mortos = {}

                    erros = 0
                    apks = ler_apks(caminho_base + 'mutantes/' + app[3])
                    lista_op_mutantes = ler_log_mutantes(app[3] + '-mutants.log')

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
                            #capturar figura
                            match = re.search(r'\/[\w.-]+-debug\d+.apk', apk_mutante)
                            fig_mutante = match.group()[1:-4] + '-ini.png'
                            time.sleep(1)
                            capturar_tela(self.__pasta + 'telas/', fig_mutante)

                            # comparar mutante com original antes dos testes
                            similar = comparar_imagens(self.__pasta + 'telas/', fig_original_ini, fig_mutante)

                            if similar:
                                tool.execute([log, app[1]])
                                fig_mutante = match.group()[1:-4] + '.png'

                                # print fig_mutante
                                capturar_tela(self.__pasta + 'telas/', fig_mutante)

                                # comparar mutante com original apos testes
                                similar = comparar_imagens(self.__pasta + 'telas/', fig_original, fig_mutante)

                            resultado.append([app[3], similar])
                            logging.info(fig_original + ', ' + fig_mutante + ', ' + str(similar))

                            # operador de mutacao
                            num_mutante = re.search(r'[0-9]+', fig_mutante).group()
                            ind = lista_op_mutantes[num_mutante]
                            if not ind in op_mutantes_total:
                                op_mutantes_total[ind] = 1
                            else:
                                op_mutantes_total[ind] += 1
                            if not similar:
                                if not ind in op_mutantes_mortos:
                                    op_mutantes_mortos[ind] = 1
                                else:
                                    op_mutantes_mortos[ind] += 1

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
                    logging.info(str(op_mutantes_mortos))
                    logging.info(str(op_mutantes_total))
                    m = 0
                    if tm > 0:
                        m = float(dm) / float(tm)
                        print 'escore de mutacao: ' + str(float(dm) / float(tm))
                    else:
                        print '[==> ATENÇÃO]: Total de mutantes válidos: 0'
                    print 'erros: ' + str(erros)
                    scores_mutacao.append([tm, m, erros])

                    # gravar nos arquivos
                    arquivo.writerow([resultado])
                    arquivo.writerow(['total de mutantes', 'score de mutacao', 'erros'])
                    arquivo.writerow([tm, m, erros])
                    arquivo.writerow(['mutantes mortos'])
                    arquivo.writerow([str(op_mutantes_mortos)])
                    arquivo.writerow(['total de mutantes'])
                    arquivo.writerow([str(op_mutantes_total)])
                    logging.info('Termino-log: ' + datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
            # media.append()
            logging.info(str(scores_mutacao))

            media_tm = 0
            media_escores = 0
            media_erros = 0
            for res in scores_mutacao:
                media_tm += res[0]
                media_escores += res[1]
                media_erros += res[2]
            print '------ MEDIAS -------'
            logging.info('------ MEDIAS -------')
            print 'total mutantes: ' + str(float(media_tm)/float(5))
            logging.info('total mutantes: ' + str(float(media_tm)/float(5)))
            print 'total escores: ' + str(float(media_escores)/float(5))
            logging.info('total escores: ' + str(float(media_escores)/float(5)))
            print 'total erros: ' + str(float(media_erros)/float(5))
            logging.info('total erros: ' + str(float(media_erros)/float(5)))
