# -*- coding: utf-8 -*-
import datetime
import logging
import os

from tool import Tool
from tools.monkey import Monkey
from tools.stoat import Stoat


# [apk, app, activity, log]
APPS = [
        ['TranslateActivity-debug', 'com.beust.android.translate',    '/.TranslateActivity',      'translate']]#,
        # ['TippyTipper-debug', 'net.mandaria.tippytipper', '/.activities.TippyTipper', 'tippytipper'],
        # ['arXiv-debug',             'com.commonsware.android.arXiv',  '/.arXiv',                  'arxiv'],
        # ['ListLentObjects-debug',   'de.freewarepoint.whohasmystuff', '/.ListLentObjects',        'whohasmystuff']]

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
    tool = Tool(pasta)
    tool.execute(Monkey(), APPS)
    # tool.execute(Stoat(), APPS)
    logging.info('Termino: ' + datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))


if __name__ == "__main__":
    main()
