# -*- coding: utf-8 -*-
import sys
import os


class Axado(object):

    def __init__(self, origem, destino, nota,
                 peso):
        """
        Setando os atributos da classe
        """
        self.origem = origem
        self.destino = destino
        self.nota = nota
        self.peso = peso
        self.path = self.get_path()

    def get_path(self):
    	"""
        valida se retorna o path do arquivo
        """
        self.path = os.path.dirname(os.path.abspath(__file__))


def get_parametros(args=[]):
    """
    Reponsável por gerar os parametros passados
    na chamado do arquivo.
    """
    if type(args) is list and len(args) == 5:
        return {"origem": args[1],
                "destino": args[2],
                "nota": args[3],
                "peso": args[4]}
    else:
        return "Erro nos parametros passados"


if __name__ == '__main__':
    params = get_parametros(sys.argv)

    if type(params) is dict:
        axado = Axado(**params)
    else:
        print params
