import json
from random import (choice, randint)
from datetime import (timedelta, datetime)
from pprint import (pprint)
from copy import (copy as CopiaObjeto)

# O banco de dados dele é uma lista que contém todas pessoas já cadastradas pelo programa. Dentro dele,
# cada cadastro será um dicionário do tipo 'string' e 'tupla'. A string é equivalente ao nome do 
# paciente, já a tupla algumas informações adicionais, como: data e hora do cadastro; o nível de 
# gravidade; e a idade dele.
CAMINHO_DO_BANCO = "dados/cadastros.json"
LISTA_DE_NOMES = "dados/testes/lista-de-nomes.txt"
BANCO_DE_DADOS_CADASTROS = []


def adiciona_cadastro(registro: dict) -> None:
    "Apenas adiciona um 'cadastro' dado no banco de dados carregado na memória."
    assert isinstance(registro, dict)
    global BANCO_DE_DADOS_CADASTROS

    BANCO_DE_DADOS_CADASTROS.append(registro)

def cadastro_palatavel_pra_json(registro: dict) -> dict:
    """
      Como JSON não aceitam 'datetime' em sí, vamos converter-los para 'float'
    O dicionário aqui passado é alterado. A função também retorna a referência
    do  mesmo objeto.
    """
    dicio = registro
    
    if __debug__:
        pprint(dicio)
        
    for nome in registro:
            criacao = dicio[nome]["criação"]
            modificado = dicio[nome]["modificação"]

            dicio[nome]["criação"] = criacao.timestamp()
            dicio[nome]["modificação"] = modificado.timestamp()
           
    return registro
   
def salva_banco_de_dados() -> None:
    """
      Salva todas modificações ou inserções no 'banco de cadastros' em disco.
    Antes disso, ele modifica o tipo de dado 'datetime' no seu 'timestamp', este
    que é um 'float', já que o JSON não é capaz inicialmente de armazenar tal tipo
    de dado estruturado. Nada será retornado.
    """
    global BANCO_DE_DADOS_CADASTROS
    # Clone da lista com dicionários atuais. Assim, não modificará o que está
    # rodando na memória. Se não fizess isso, causaria um problema de 'datarace'.
    lista_de_cadastros_ajustados = CopiaObjeto(BANCO_DE_DADOS_CADASTROS)

    # Transformando cada 'datetime' no seu 'timestamp'(um decimal).
    for dicio in lista_de_cadastros_ajustados:
        cadastro_palatavel_pra_json(dicio)

    # Gravando a lista de dados no respectivo caminho que foi dado.
    arquivo = open(CAMINHO_DO_BANCO, "wt", encoding="utf8")
    json.dump(lista_de_cadastros_ajustados, arquivo, indent=4)
    arquivo.close()
    print("Os cadastros foram salvos com sucesso.")

def carrega_banco_de_dados() -> None:
    """
      Carrega o banco de dados no disco(um arquivo JSON), para a variável global
    'BANCO_DE_DADOS_CADASTROS', que está rodando na memória. É bom chamar esta função
    apenas uma vez por execução, se não, irá causar conflitos ou duplicação de
    dados. Observe que o algoritmo não apaga as outras já carregadas, apenas adiciona 
    novas.
    """
    global BANCO_DE_DADOS_CADASTROS

    # Abre o arquivo do caminho específicado. Então atribui a lista decodificada
    # na variável global que registra os cadastros em tempo de execução.
    arquivo = open(CAMINHO_DO_BANCO, "rt", encoding="utf8")
    lista_resultado = json.load(arquivo)
    arquivo.close()

    # Modifica novamente o 'timestamp' para um 'datetime'.
    for dicio in lista_resultado:
        for nome in dicio:
            criacao = dicio[nome]["criação"]
            modificado = dicio[nome]["modificação"]

            dicio[nome]["criação"] = datetime.fromtimestamp(criacao)
            dicio[nome]["modificação"] = datetime.fromtimestamp(modificado)
            BANCO_DE_DADOS_CADASTROS.append(dicio)
    print("O banco de dados foi carregado com sucesso.")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
from unittest import (TestCase)

class SalvandoAlgunsRegistros(TestCase):
    def setUp(self):
        global LISTA_DE_NOMES

        self.nomes_arquivo = open(LISTA_DE_NOMES, "rt", encoding="utf8")
        self.conteudo = self.nomes_arquivo.read().split('\n')
        self.nomes_arquivo.close()

    def tearDown(self):
        pass

    def seleciona_nome_aleatorio(self) -> str:
        return choice(self.conteudo).rstrip('\n')

    def datetime_aleatorio(self) -> datetime:
        return datetime(
            hour=randint(0, 23),
            minute=randint(0, 60),
            second=randint(0, 60),
            # O hospital existe desde a década de 80.
            year=randint(1980, 2026),
            month=randint(1, 12),
            day=randint(1, 28)
        )
    def cria_cadastro_aleatorio(self) -> dict:
        nome = self.seleciona_nome_aleatorio()
        criacao = self.datetime_aleatorio()
        modificacao = criacao 
        idade = randint(1, 70)
        nivel = randint(1, 5)

        return {
            f"{nome}": {
                "idade": idade,
                "estado": nivel,
                "criação": criacao,
                "modificação": modificacao
            }
        }

    def runTest(self):
        pprint(BANCO_DE_DADOS_CADASTROS)
        for _ in range(4):
            instancia = self.cria_cadastro_aleatorio()
            adiciona_cadastro(instancia)

        pprint(BANCO_DE_DADOS_CADASTROS)
        salva_banco_de_dados()

class CarregandoBancoDeDados(TestCase):
    def runTest(self):
        global BANCO_DE_DADOS_CADASTROS

        carrega_banco_de_dados()
        pprint(BANCO_DE_DADOS_CADASTROS)

class MexendoComJSON(TestCase):
    def runTest(self):
        with open(CAMINHO_DO_BANCO, "wt") as database:
            amostras = [
                {'nada': 'alguma coisa'},
                {'amanda': [15, 27]},
                {"vitor": datetime.today().timestamp()}
            ]
            json.dump(amostras, database, indent=5)