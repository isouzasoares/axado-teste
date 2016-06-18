# -*- coding: utf-8 -*-
import sys
import os
import unicodecsv
import re
# resgata o diretorio atual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class CsvObject(object):

    def __init__(self, path, preco=None):
    	"""
        Setando os atributos da classe
        """
        self.path = path
        self.dados = {}
        self.cria_objeto_csv()

    def cria_objeto_csv(self):
    	"""
        Faz a leitura do arquivo csv ou tsv e retorna
        em formato de objeto
        """
        # utilizado caso nao encontre o file
        try:
            # lista so arquivos do diretorio do path
            for arquivo in os.listdir(self.path):
                delimit = ','
                # Verifica se há .tsv no caminho do file
                if arquivo.endswith('.tsv'):
                    delimit = '\t'
                # remove a extensao do nome para colocar na key do objeto
                nome_dict = re.sub("(.csv|.tsv)", '', arquivo)
                # Tenta executar a leitura do arquivo csv
                with open(self.path + arquivo) as csvfile:
                    reader = unicodecsv.DictReader(csvfile, delimiter=delimit)
                    self.dados[nome_dict] = [dado for dado in reader]
        except OSError:
            return "Arquivo não encontrado"

    def filtro_precos(self, nome, preco=None):
        """
        Executa o filtro por preços
        """
        # Normalizando os valores para o filtro
        nome = nome.lower()
        items = []
        if self.dados:
            # Executando o filtro=
            for i in self.dados.get('preco_por_kg'):
                if i.get('nome').lower() == nome:
                    items.append(i)
        return items

    def filtro_rotas(self, origem, destino):
        """
        Executa o filtro utilizando os campos item_um
        e item_dois, caso seja preco ele muda a regra
        """
        # Normalizando os valores para o filtro
        origem = origem.lower()
        destino = destino.lower()
        items = []
        if self.dados:
            # Executando o filtro de acordo com o digitado
            # valida a regra que sera utilizada
            for i in self.dados.get('rotas'):
                # Executa o filtro de acrodo com os campos passados
                if (i.get('origem', '').lower() == origem and
                   i.get('destino', '').lower() == destino):
                    i['precos'] = self.filtro_precos(i['kg'])
                    items.append(i)
        return items


class Axado(object):

    def __init__(self, origem, destino, nota,
                 peso, tabela=1):
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
