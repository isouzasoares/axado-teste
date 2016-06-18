# -*- coding: utf-8 -*-
import sys
import os
import unicodecsv
import re
# resgata o diretorio atual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class CsvObject(object):

    def __init__(self, path, peso=''):
        """Setando os atributos da classe"""
        self.path = path
        self.dados = {}
        self.peso = peso
        self.cria_objeto_csv()

    def cria_objeto_csv(self):
    	"""Faz a leitura do arquivo csv ou tsv e retorna
           em formato de objeto"""
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

    def cvs_valor(self, valor):
        """retorna o valor convertido pra float"""
        # Responsável por validar se vai converter normalmente
        try:
            return float(valor)
        except ValueError:
            return '-'

    def filtro_precos(self, nome):
        """Executa o filtro por preços"""
        # Normalizando os valores para o filtro
        nome = nome.lower()
        if self.dados:
            # Executando o filtro
            for i in self.dados.get('preco_por_kg'):
                if i.get('nome').lower() == nome:
                    inicial = self.cvs_valor(i.get('inicial'))
                    final = self.cvs_valor(i.get('final'))
                    valor = self.cvs_valor(self.peso)
                    # Valida a faixa de peso para retornar o preço correto
                    if ((type(final) is float and type(inicial) is float) and
                       ((valor >= inicial) and (valor < final))) or\
                       ((type(inicial) is float and type(final) is str) and
                       (valor >= inicial)):
                        return i
        return {}

    def filtro_rotas(self, origem, destino):
        """Executa o filtro utilizando os campos item_um
           e item_dois, caso seja preco ele muda a regra"""
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
                 peso, tabela='tabela'):
        """Seta os atributos da classe"""
        self.origem = origem
        self.destino = destino
        self.nota = nota
        self.peso = peso
        self.tabela = tabela
        path_tabela = '/{0}/'.format(self.tabela)
        # Valida qual diretorio ele vai acessar
        if tabela == 1:
            self.dados = CsvObject(BASE_PATH + path_tabela, self.peso)
        else:
            self.dados = CsvObject(BASE_PATH + path_tabela, self.peso)
        valores = self.dados.filtro_rotas(self.origem, self.destino)
        if valores:
            self.dados = valores[0]
        else:
            self.dados = {}

    def get_seguro(self):
        """retorna o valor do seguro"""
        # Caso dê um erro na conversão
        try:
            return float(self.nota) * float(self.dados.get('seguro', '')) / 100
        except (ValueError, TypeError):
            return '-'

    def get_faixa(self):
        """retorna o valor total da faixa"""
        # Caso dê um erro na conversão
        try:
            preco = self.dados.get('precos', {}).get('preco')
            return float(self.peso) * float(preco)
        except (ValueError, TypeError):
            return '-'

    def get_subtotal(self):
        """retorna o valor subtotal"""
        # Caso dê um erro na conversão
        try:
            fixa = self.dados.get('fixa')
            seguro = self.get_seguro()
            sub = float(seguro) + float(fixa) + float(self.get_faixa())
            return sub
        except (ValueError, TypeError):
            return '-'

    def get_frete(self):
        """retorna o calculo """
        # Caso dê um erro na conversão
        try:
            icms = self.dados.get('icms') if self.dados.get('icms') else 6
            total = self.get_subtotal() / ((100 - float(icms)) / 100)
            return "%.2f" % total
        except (ValueError, TypeError):
            return '-'


def get_parametros(args=[]):
    """Reponsável por gerar os parametros passados
       na chamado do arquivo."""
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
