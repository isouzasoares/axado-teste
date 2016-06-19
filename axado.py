# -*- coding: utf-8 -*-
import sys
import os
import unicodecsv
import re
from decimal import Decimal, ROUND_UP
# resgata o diretorio atual
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class CsvObject(object):

    def __init__(self, path):
        """Setando os atributos da classe"""
        self.path = path
        self.dados = {}
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
        """Retorna o valor convertido pra float"""
        try:
            return float(valor)
        except ValueError:
            return '-'

    def filtro_precos(self, nome, peso):
        """Executa o filtro por preços"""
        # Normalizando os valores para o filtro
        nome = nome.lower()
        if self.dados:
            # Executando o filtro
            for i in self.dados.get('preco_por_kg'):
                if i.get('nome').lower() == nome:
                    inicial = self.cvs_valor(i.get('inicial'))
                    final = self.cvs_valor(i.get('final'))
                    valor = self.cvs_valor(peso)
                    # Valida a faixa de peso para retornar o preço correto
                    if ((type(final) is float and type(inicial) is float) and
                       ((valor >= inicial) and (valor < final))) or\
                       ((type(inicial) is float and type(final) is str) and
                       (valor >= inicial)):
                        return i
        return {}

    def filtro_rotas(self, origem, destino, peso):
        """Executa o filtro utilizando os campos item_um
           e item_dois, caso seja preco ele muda a regra"""
        # Normalizando os valores para o filtro
        origem = origem.lower()
        destino = destino.lower()
        items = []
        if self.dados:
            # Executando o filtro de acordo com o digitado
            for i in self.dados.get('rotas'):
                # Executa o filtro de acordo com os campos passados
                limite = self.cvs_valor(i.get('limite', 0))
                if (i.get('origem', '').lower() == origem and
                   i.get('destino', '').lower() == destino) and\
                   ((limite and peso <= limite) or
                   limite == 0):
                    i['precos'] = self.filtro_precos(i['kg'], peso)
                    items.append(i)
        return items


class Axado(object):

    def __init__(self, origem, destino, nota,
                 peso, tabela='tabela'):
        """Seta os atributos da classe"""
        self.origem = origem
        self.destino = destino
        self.nota = nota
        self.peso = float(peso)
        self.tabela = tabela
        path_tabela = '/{0}/'.format(self.tabela)
        csv_object = CsvObject(BASE_PATH + path_tabela)
        self.dados = csv_object.filtro_rotas(self.origem, self.destino,
                                             self.peso)
        if self.dados:
            self.dados = self.dados[0]
        else:
            self.dados = {}
        self.prazo = self.dados.get('prazo', '-')

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
            # se tiver fixa na tabela ele resgata
            # caso contrário ele seta 0 para soma
            fixa = self.dados.get('fixa') if self.dados.get('fixa') else 0
            seguro = self.get_seguro()
            sub = float(seguro) + float(fixa) + float(self.get_faixa())
            if self.dados.get('alfandega'):
                alfandega = sub * (float(self.dados.get('alfandega')) / 100)
                sub += alfandega
            return sub
        except (ValueError, TypeError):
            return '-'

    def get_total(self):
        """retorna o calculo total"""
        # Caso dê um erro na conversão
        try:
            icms = self.dados.get('icms') if self.dados.get('icms') else 6
            total = self.get_subtotal() / ((100 - float(icms)) / 100)
            if type(total) is float:
                # Converte valor para exibição arredondado
                total = Decimal(total)
                total = float(total.quantize(Decimal('.01'),
                              rounding=ROUND_UP))
                return total
        except (ValueError, TypeError):
            return '-'

    def get_frete(self):
        """retorna o frete para saida no terminal"""
        total = self.get_total()
        # Verifica se o valor total é float para conversão correta
        if type(total) is float:
            return "%s:%s, %.2f" % (self.tabela, self.prazo, total)
        return "%s:%s, %s" % (self.tabela, self.prazo, self.get_total())


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
        axado_one = Axado(**params)
        params['tabela'] = 'tabela2'
        axado_two = Axado(**params)
        print axado_one.get_frete()
        print axado_two.get_frete()
    else:
        print params
