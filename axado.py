# -*- coding: utf-8 -*-
import sys
import os
import unicodecsv

# resgata o diretorio atual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class CsvObject(object):

    def __init__(self, path):
    	"""
        Setando os atributos da classe
        """
        self.path = path
        self.rotas = None
        self.cria_objeto_csv()

    def cria_objeto_csv(self):
    	"""
        Faz a leitura do arquivo csv ou tsv e retorna
        em formato de objeto
        """
        # Tenta executar a leitura do arquivo csv
        try:
            with open(self.path) as csvfile:
                reader = unicodecsv.DictReader(csvfile)
                self.rotas = [i for i in reader]
        except IOError:
            return "Arquivo não encontrado"


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


def get_parametros(args=[]):
    """
    Reponsável por gerar os parametros passados
    na chamado do arquivo.
    """
    # valida se há args
    if type(args) is list and len(args) == 5:
        # retorna o objeto dic montado
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
