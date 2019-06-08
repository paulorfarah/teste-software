#-*- coding: utf-8 -*-
from tools.eventos import executar_evento


class Stoat(object):

    def execute(self, params):
        f = open(params[0], 'r')
        f1 = f.readlines()
        for l in f1:
            executar_evento(l)
