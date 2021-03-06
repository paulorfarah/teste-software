# -*- coding: utf-8 -*-
import datetime
import logging
import os

from tool import Tool
from tools.ape import Ape
from tools.eventos_avc import teste
from tools.monkey import Monkey
from tools.stoat import Stoat


# [apk, app, activity, log_stoat, log_mdroid+]
APPS = [
        #['TranslateActivity-debug', 'com.beust.android.translate', '/.TranslateActivity', 'translate'],
         #['TippyTipper-debug', 'net.mandaria.tippytipper', '/.activities.TippyTipper', 'tippytipper'],
         #['arXiv-debug', 'com.commonsware.android.arXiv', '/.arXiv', 'arxiv']#,
          ['ListLentObjects-debug', 'de.freewarepoint.whohasmystuff', '/.ListLentObjects', 'whohasmystuff']
        ]

def criar_pasta():
    # criar pastas
    if not os.path.exists('resultados/'):
        os.makedirs('resultados/')
    pasta = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    if not os.path.exists('resultados/' + pasta):
        os.makedirs('resultados/' + pasta)
        os.makedirs('resultados/' + pasta + '/telas')
    return pasta



def main():
    pasta = criar_pasta()
    # logging
    logging.basicConfig(filename='resultados/' + pasta + '/resultados.log', level=logging.INFO)
    logging.info('Inicio: ' + datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    # testes
    # teste() #teste com AndroidViewClient
    tool = Tool(pasta)
    # tool.execute(Monkey(), APPS)
    # tool.execute(Stoat(), APPS)
    tool.execute(Ape(), APPS)
    logging.info('Termino: ' + datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))


if __name__ == "__main__":
    main()
