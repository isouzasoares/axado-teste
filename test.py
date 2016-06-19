# -*- coding: utf-8 -*-
import unittest
from axado import Axado, get_parametros, CsvObject, BASE_PATH
from decimal import Decimal, ROUND_UP


class TestAxado(unittest.TestCase):

    def setUp(self):
    	"""Inicializador da variavel que será
           usado durante o teste, de acordo com as
           planilhas
        """
        # Instanciando a classe Axado para
        # uso durante o processo de test
        # Os testes poderiam ser desvinculados da planilha, basta setar
        # para self.axado.valores um objeto parecido com o gerado para
        # essa origem e destino, já testado em TestCsvObject
        self.axado = Axado('florianopolis', 'brasilia', '50', '7', 'tabela')
        # Instanciando tabela 2
        self.axado_d = Axado('florianopolis', 'brasilia', '50', '7', 'tabela2')

    def test_param_error(self):
        """Valida a geração dos parametros errado passados
           na chamado do arquivo axado.py
        """
        # deixando parametros vazio
        param = get_parametros()
        self.assertEquals(param, 'Erro nos parametros passados')
        # passa parametro de qualquer maneira
        param = get_parametros('menor exigido')
        self.assertEquals(param, 'Erro nos parametros passados')
        # passando lista menor que o exigido
        param = get_parametros(['a', 'b', 'c'])
        self.assertEquals(param, 'Erro nos parametros passados')

    def test_param(self):
        """Valida parametro passado de maneira correta"""
        # seta os parametros corretos
        list_param = ['axado.py', 'florianopolis', 'brasilia', '50', '7']
        # executa a def para resgate do objeto de parametros montado
        param = get_parametros(list_param)
        self.assertEquals(type(param), dict)

    def test_subtotal(self):
        """Valida se o subtotal está correto"""
        # 98.5 levando em consideração a planilha e a lógica das fórmulas
        self.assertEquals(self.axado.get_subtotal(), 98.5)
        axado = Axado('Belo horizonte', 'brasilia', '50', '7', 'tabela')
        self.assertEquals(axado.get_subtotal(), '-')

    def test_seguro(self):
        """Valida o retorno do seguro"""
        self.assertEquals(self.axado.get_seguro(), 1.5)
        axado = Axado('Belo horizonte', 'brasilia', '50', '7', 'tabela')
        self.assertEquals(axado.get_seguro(), '-')

    def test_faixa(self):
        """Valida o retorno de faixa"""
        self.assertEquals(self.axado.get_faixa(), 84)
        axado = Axado('Belo horizonte', 'brasilia', '50', '7', 'tabela')
        self.assertEquals(axado.get_faixa(), '-')

    def test_total(self):
        """Valida o retorno do total"""
        # Valores setado a mão seguindo a lógica do glossário e planilha
        # Valida se o sistema está retornando valor arrendodado
        total = 98.5 / ((100 - float(6)) / 100)
        self.assertNotEquals(self.axado.get_total(), total)
        # Valida se total está correto
        total = Decimal(total)
        total = float(total.quantize(Decimal('.01'), rounding=ROUND_UP))
        self.assertEquals(self.axado.get_total(), total)
        axado = Axado('Belo horizonte', 'brasilia', '50', '7', 'tabela')
        # Valida se a maneira errada realmente retorna um traçço
        self.assertEquals(axado.get_total(), '-')

    def test_frete(self):
        """Valida se o retorno da string de frete é a esperada"""
        # Validando resposta em string dos valores
        self.assertEquals(self.axado.get_frete(), "tabela:3, 104.79")
        self.assertNotEquals(self.axado_d.get_frete(), "tabela:3, 104.79")


class TestCsvObject(unittest.TestCase):

    def test_path_nao_encontrado(self):
        """Valida se o path dos arquivos existe"""
        # instancia o objeto com caminho de path errado
        csv_dict = CsvObject('fdfdas/b/c')
        self.assertEquals(len(csv_dict.dados), 0)

    def test_path_csv_tsv(self):
        """Valida se retorna objeto caso o path seja encontrado"""
        # instancia o objeto com caminho de path correto
        csv_dict = CsvObject(BASE_PATH + '/tabela/')
        # valida se retornou a lista de itens
        self.assertEquals(type(csv_dict.dados), dict)
        # verifica se retorna pelo menos 1 objeto
        self.assertTrue(len(csv_dict.dados) > 0)
        # verifica se realizou a leitura do tsv
        tsv_file = CsvObject(BASE_PATH + '/tabela2/')
        self.assertTrue(len(tsv_file.dados) > 0)

    def test_filtro_rotas(self):
        """Executa o teste de filtro para origem e destino"""
        csv_dict = CsvObject(BASE_PATH + '/tabela/')
        origem = 'florianopolis'
        destino = 'brasilia'
        peso = 7
        self.assertTrue(len(csv_dict.filtro_rotas(origem, destino, peso)) > 0)
        origem = 'Belo horizonte'
        destino = 'brasilia'
        self.assertListEqual(csv_dict.filtro_rotas(origem, destino, peso), [])

    def test_filtro_precos(self):
        """Executa teste do filtro de preços por peso"""
        # instanciando para tabela do tipo 1
        csv_dict = CsvObject(BASE_PATH + '/tabela/')
        nome = 'flo'
        peso = 7
        # Verifica se o retorno é do tipo dict
        self.assertEquals(type(csv_dict.filtro_precos(nome, peso)), dict)
        self.assertEquals(csv_dict.filtro_precos(nome, peso).get('preco'),
                          '12')
        # Verificações se o filro está retornando de maneira consistente
        peso = '9.99'
        self.assertEquals(csv_dict.filtro_precos(nome, peso).get('preco'),
                          '12')
        peso = '11'
        self.assertEquals(csv_dict.filtro_precos(nome, peso).get('preco'),
                          '11')
        peso = '19.99'
        self.assertEquals(csv_dict.filtro_precos(nome, peso).get('preco'),
                          '11')

    def test_limit_peso(self):
        """Executa o teste de limite de peso para o tipo tabela 2"""
        # Instanciando a tabela do tipo 2
        tsv_file = CsvObject(BASE_PATH + '/tabela2/')
        # Seta um peso fora do limite
        origem = 'saopaulo'
        destino = 'florianopolis'
        peso = 130
        self.assertListEqual(tsv_file.filtro_rotas(origem, destino, peso),
                             [])
        # Valida se peso passou pela regra de limite
        peso = 100
        self.assertTrue(len(tsv_file.filtro_rotas(origem, destino, peso)) > 0)
if __name__ == '__main__':

    # executa os testes
    unittest.main(verbosity=2)
