# -*- coding: utf-8 -*-
import unittest
from axado import Axado, get_parametros, CsvObject, BASE_PATH


class TestAxado(unittest.TestCase):

    def setUp(self):
    	"""
        Inicializador da variavel que será
        usado durante o teste
        """
        # Instanciando a classe Axado para
        # uso durante o processo de test
        self.axado = Axado('a', 'b', 'c', 'd')

    def test_path(self):
    	"""
        Valida se há path
        """
        self.assertFalse('', BASE_PATH)

    def test_param_error(self):
        """
        Valida a geração dos parametros errado passados
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
        """
        Valida parametro passado de maneira correta
        """
        # seta os parametros corretos
        list_param = ['axado.py', 'florianopolis', 'brasilia', '50', '7']
        # executa a def para resgate do objeto de parametros montado
        param = get_parametros(list_param)
        self.assertEquals(type(param), dict)


class TestCsvObject(unittest.TestCase):

    def test_path_nao_encontrado(self):
        """
        Valida se o path dos arquivos existe
        """
        # instancia o objeto com caminho de path errado
        csv_dict = CsvObject('fdfdas/b/c')
        self.assertIsNone(csv_dict.dados)

    def test_path_csv_tsv(self):
        """
        Valida se retorna objeto caso o path seja encontrado
        """
        # instancia o objeto com caminho de path correto
        csv_dict = CsvObject(BASE_PATH + '/tabela/rotas.csv')
        # valida se retornou a lista de itens
        self.assertEquals(type(csv_dict.dados), list)
        # verifica se retorna pelo menos 1 objeto
        self.assertTrue(len(csv_dict.dados) > 0)
        # verifica se realizou a leitura do tsv
        tsv_file = CsvObject(BASE_PATH + '/tabela2/rotas.tsv')
        self.assertTrue(len(tsv_file.dados) > 0)

    def test_filtro_rotas(self):
        """
        Executa o teste de filtro para origem e destino
        """
        csv_dict = CsvObject(BASE_PATH + '/tabela/rotas.csv')
        origem = 'florianopolis'
        destino = 'brasilia'
        self.assertTrue(len(csv_dict.filtro_dados(origem, destino)) > 0)
        origem = 'Belo horizonte'
        destino = 'brasilia'
        self.assertEquals(csv_dict.filtro_dados(origem, destino), [])

    def teste_filtro_preco(self):
        """
        Executa o teste por filtro para preco e nome
        """
        csv_dict = CsvObject(BASE_PATH + '/tabela2/preco_por_kg.tsv')
        nome = 'flo'
        self.assertTrue(len(csv_dict.filtro_dados(nome)) > 0)
        nome = 'a'
        self.assertFalse(len(csv_dict.filtro_dados(nome)) > 0)

if __name__ == '__main__':

    # executa os testes
    unittest.main()
