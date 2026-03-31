'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada 
  pela gravidade.
'''

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo dos Modelos
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
from dataclasses import dataclass
from datetime import (datetime as DateTime)

@dataclass
class Cadastro:
	"""
		Claro que este modelo é para o futuro. Como ele ensinou apenas dicionário até o momento, farei
	exatamente assim. Então, cada cadastro feito, será colocado num dicionário, onde a chave é o 'nome',
	e o valor dela será uma tupla com os demais dados.
	"""
    # Campos da instrução do trabalho.
	nome: str
	idade: int
	nivel: int
	# Campos extras que sugiro:
	criado: DateTime
	modificacoes: tuple[int, Datetime]
 
	# Métodos necessários de definir, se não a função/method 'sort' não irá funcionar.
	def __le__(self, outro: Self) -> bool:
		return self.nivel <= outro.nivel
    
	def __ge__(self, outro: Self):
 		return self.nivel >= outro.nivel

	def __lt__(self, outro: Self) -> bool:
    		return self.nivel < outro.nivel
    
	def __gt__(self, outro: Self):
 		return self.nivel > outro.nivel

	# Métodos de serialização dos tipos de dados:
	def serializar(self) -> bytearray:
		pass

	@staticmethod
	def deserializar(dados: bytearray) -> Self:
		pass

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo do Banco de Dados
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
# O banco de dados dele é uma lista que contém todas pessoas já cadastradas pelo programa. Dentro dele,
# cada cadastro será um dicionário do tipo 'string' e 'tupla'. A string é equivalente ao nome do 
# paciente, já a tupla algumas informações adicionais, como: data e hora do cadastro; o nível de 
# gravidade; e a idade dele.
CAMINHO_DO_BANCO = "dados/cadastros.dat"
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
NOME_DO_HOSPITAL = "Centro Hospitalar Acadêmico Silva Brandão"


"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
							Módulo Específico a Interface
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
import shutil

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
    
# Testes iniciais das funções. Futuramente, colocar tudo isso no 'TestCase' do 'unittest', que
# é uma biblioteca Python específica para testes unitários:
mostrar_cabecalho_em_caixa("Sistema de Triagem de Pacientes")
mostrar_cabecalho("Sistema de Triagem de Pacientes")
cabecalho_padrao_do_hospital()
visualizacao_do_menu("Obituário", "Cadastrar", "Remover", "Listagem", "Informação", "Status")