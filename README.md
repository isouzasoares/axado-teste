Cálculo de frete axado
======================

Teste axado para cálculo de fretes, de acordo com os dados pré cadastrados nas planilhas.

Quickstart
---------------

Versão do python compatível:
```
python 2.7
```

Use virtualenv ::
```
 É aconselhavél que se utilize virtual env, para montagem do ambiente de execução.
```
 - https://virtualenv.pypa.io/en/stable/

Clone do reposítório ::
```
git clone https://github.com/isouzasoares/axado-teste
cd axado-teste
pip install -r requirements.txt
```

Execução dos testes ::
```
Dentro de axado-teste:
python test.py
```

Calculando o frete ::
```
Dentro de axado-teste:
python axado.py <origem> <destino> <nota_fiscal> <peso>
```