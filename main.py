'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada
  pela gravidade.
'''

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo do Banco de Dados
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
from unittest import (TestCase)
import json
from random import (choice, randint)
from datetime import (datetime)
from pprint import (pprint)
from copy import (copy as CopyObj)

# O banco de dados dele é uma lista que contém todas pessoas já cadastradas pelo programa. Dentro dele,
# cada cadastro será um dicionário do tipo 'string' e 'tupla'. A string é equivalente ao nome do 
# paciente, já a tupla algumas informações adicionais, como: data e hora do cadastro; o nível de 
# gravidade; e a idade dele.
CAMINHO_DO_BANCO = "dados/cadastros.json"
LISTA_DE_NOMES = "dados/testes/lista-de-nomes.txt"
BANCO_DE_DADOS_CADASTROS = []
# Nome genérico que "inventei". Na verdade, pedir para o 'Gemini' criar tal, mas baseado no seguinte
# prompt: "Pode sugerir-me um nome de hospital, um que remeta a uma instituição antiga e respeitada."
# A resposta dele foi a seguinte lista, e mais paragrafos e paragros de explicação porque estas escolhas:
#
#    Hospital Memorial Cândido Ferreira
#    Centro Hospitalar Acadêmico Silva Brandão
#    Real Beneficência da Colina
#    Hospital da Santa Perseverança
#    Sociedade Hospitalar Dom Pedro II
#    Hospital Sancta Vita
#    Hospital Magnus Curatio
#    Instituto Salus

def adiciona_cadastro(registro: dict) -> None:
    assert isinstance(registro, dict)
    global BANCO_DE_DADOS_CADASTROS

    BANCO_DE_DADOS_CADASTROS.append(registro)

def salva_banco_de_dados() -> None:
    global BANCO_DE_DADOS_CADASTROS
    # Clone da lista com dicionários atuais:
    lista_de_cadastros_ajustados = CopyObj(BANCO_DE_DADOS_CADASTROS)

    for dicio in lista_de_cadastros_ajustados:
        for nome in dicio:
            dicio[nome]["criação"] = dicio[nome]["criação"].timestamp()
            dicio[nome]["modificação"] = dicio[nome]["modificação"].timestamp()

    arquivo = open(CAMINHO_DO_BANCO, "wt", encoding="utf8")
    json.dump(lista_de_cadastros_ajustados, arquivo, indent=4)
    arquivo.close()

def carrega_banco_de_dados() -> None:
    global BANCO_DE_DADOS_CADASTROS

    arquivo = open(CAMINHO_DO_BANCO, "rt", encoding="utf8")
    lista_resultado = json.load(arquivo)
    arquivo.close()

    for dicio in lista_resultado:
        for nome in dicio:
            criacao = dicio[nome]["criação"]
            modificado = dicio[nome]["modificação"]

            dicio[nome]["criação"] = datetime.fromtimestamp(criacao)
            dicio[nome]["modificação"] = datetime.fromtimestamp(modificado)
            BANCO_DE_DADOS_CADASTROS.append(dicio)

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
"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo Específico a Interface
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
import shutil

NOME_DO_HOSPITAL = "Centro Hospitalar Acadêmico Silva Brandão"

def barra_do_tamanho_da_tela(componente: str) -> str:
    LARGURA_TELA = shutil.get_terminal_size().columns - 5
    
    return componente * LARGURA_TELA

def mostrar_cabecalho_em_caixa(titulo: str) -> None:
    """
    Está função formata e imprime um cabeçalho qualquer, dado a string que você colocou como argumento.
    O mesmo que a função 'mostrar_cabecalho', entretanto, este a formatação dela é diferente, ele faz
    a string ficar centralizado entre as barras.
    """
    # Apenas aceita argumentos do tipo string.
    assert isinstance(titulo, str)
    
    comprimento = len(titulo)
    LARGURA_TELA = shutil.get_terminal_size().columns - 5
    qtd_tracos = (LARGURA_TELA - comprimento) // 2
    barra = '-' * LARGURA_TELA
    recuo = ' ' * qtd_tracos
    
    print(f"\n{barra}\n{recuo}{titulo}\n{barra}\n")

def mostrar_cabecalho(titulo: str) -> None:
    """
    Está função formata e imprime um cabeçalho qualquer, dado a string que você colocou como argumento.
    """
    # Apenas aceita argumentos do tipo string.
    assert isinstance(titulo, str)
    import shutil
    
    comprimento = len(titulo)
    LARGURA_TELA = shutil.get_terminal_size().columns - 5
    qtd_tracos = (LARGURA_TELA - comprimento) // 2
    barra = '-' * qtd_tracos
    
    print(f"\n{barra} {titulo} {barra}\n")


def visualizacao_do_menu(*todas_opcoes) -> None:
    # Um contador.
    cursor = 1
    # Máximo de colunas permitidas no menu.
    COLUNAS = 4
    
    # Cria barra e imprime a descrição, neste caso: 'menu'.
    print(barra_do_tamanho_da_tela('+'))
    print("Menu:")
    
    for (numeracao, opcao) in enumerate(todas_opcoes):
        # Condicional pula para uma nova linha, quando bater o limite de colunas
        # pré-determinado, isso pela constante 'COLUNAS'.
        if cursor % COLUNAS == 0:
            print("")
            
        print(f"\t{numeracao + 1}) {opcao}", end='')
        cursor += 1
    print('\n',barra_do_tamanho_da_tela('+'))

def cabecalho_padrao_do_hospital() -> None:
    print(f"""
        \r{barra_do_tamanho_da_tela('=')}
           	\t\tCaadastrario dos Pacientes 
        		\t\tno
			{NOME_DO_HOSPITAL}
        \r{barra_do_tamanho_da_tela('=')}
        """)
