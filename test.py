# -*- coding: utf-8 -*-

import unittest
from axado import Axado


class TestAxado(unittest.TestCase):

    def setUp(self):
    	"""
        Inicializador da variavel que será
        usado durante o teste
        """
        # Instanciando a classe Axado para
        # uso durante o processo de test
        self.axado = Axado()

if __name__ == '__main__':
    unittest.main()
