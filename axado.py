# -*- coding: utf-8 -*-
import sys
import os
import unicodecsv
# resgata o diretorio atual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class CsvObject(object):

    def __init__(self, path, preco=None):
    	"""
        Setando os atributos da classe
        """
        self.path = path
        self.dados = None
        self.cria_objeto_csv()

    def cria_objeto_csv(self):
    	"""
        Faz a leitura do arquivo csv ou tsv e retorna
        em formato de objeto
        """
        delimiter = ','
        # Verifica se há .tsv no caminho do file
        if self.path.endswith('.tsv'):
            delimiter = '\t'
        # Tenta executar a leitura do arquivo csv
        try:
            with open(self.path) as csvfile:
                reader = unicodecsv.DictReader(csvfile, delimiter=delimiter)
                self.dados = [dado for dado in reader]
        except IOError:
            return "Arquivo não encontrado"

    def filtro_dados(self, item_um, item_dois=None):
        """
        Executa o filtro utilizando os campos item_um
        e item_dois, caso seja preco ele muda a regra
        """
        # Normalizando os valores para o filtro
        item_um = item_um.lower()
        if item_dois:
            item_dois = item_dois.lower()
        items = []
        if self.dados:
            # Executando o filtro de acordo com o digitado
            # valida a regra que sera utilizada
            for i in self.dados:
                # Executa o filtro de acrodo com os campos passados
                if i.get('nome', '') == item_um or \
                   (i.get('origem', '').lower() == item_um and
                   i.get('destino', '').lower() == item_dois):
                    items.append(i)
        return items


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
    # resgatando os parametros
    params = get_parametros(sys.argv)
    # verifica se retornou um dicionario ao montar os parametros
    if type(params) is dict:
        axado = Axado(**params)
    else:
        print params
