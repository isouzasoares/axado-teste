# -*- coding: utf-8 -*-

import unittest
from axado import Axado, get_parametros


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
        self.assertFalse('', self.axado.path)

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
        list_param = ['axado.py', 'florianopolis', 'brasilia', '50', '7']
        param = get_parametros(list_param)
        self.assertEquals(type(param), dict)

if __name__ == '__main__':

    # executa os testes
    unittest.main()
