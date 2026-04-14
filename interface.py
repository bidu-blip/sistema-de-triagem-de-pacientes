# Biblioteca padrão do Python:
import shutil
from unittest import (TestCase)
from datetime import (datetime, timedelta)
# Módulos pro próprio projeto:
from bancodedados import (todos_cadastros)
from modelos import (cria_cadastro, nome_cadastro)
# Módulos de bibliotecas externas:
from externo.legivel import (tempo as tempo_legivel)

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
#NOME_DO_HOSPITAL = "Centro Hospitalar Acadêmico Silva Brandão"
NOME_DO_HOSPITAL = "Sociedade Hospitalar Dom Pedro II"

def visualizacao_do_menu(*menus: list[str]) -> None:
    """
    Pega menus feitas(uma lista), então númera os de 1 à quantia total, e formata 
    eles em colunas. Retorna nada.
    """
    assert all(map(lambda item: isinstance(item, str), menus))
    # Um contador.
    cursor = 1
    # Máximo de colunas permitidas no menu.
    COLUNAS = 4
    ESPACO = ' '
    RECUO = ESPACO * 4
    # Comprimento da maior string entre menus, assim pode espaçar cada um
    # referente a ele.
    maior = len(max(*menus))

    # Se o comprimento da string não for o suficiente, colocar um padrão.
    if maior >= 9:
        maior += 3
    else:
        maior = 7

    # Cria barra e imprime a descrição, neste caso: 'menu'.
    print(barra_do_tamanho_da_tela('+'))
    print("Menu:", end='\n\n')

    for (numeracao, opcao) in enumerate(menus):
        # Condicional pula para uma nova linha, quando bater o limite de colunas
        # pré-determinado, isso pela constante 'COLUNAS'.
        if cursor % COLUNAS == 0:
            print("")

        print(f"{RECUO}{numeracao + 1}) {opcao:<{maior}}", end='')
        cursor += 1
    # Espaçando e colocar a barra de baixo.
    print(''); print(barra_do_tamanho_da_tela('+')); print('')

def listagem_de_cadastros() -> None:
    LISTA_DE_CADASTROS = todos_cadastros() 
    total = len(LISTA_DE_CADASTROS)
    # Pula uma linha para ficar mais organizado(espaçado).
    print("")
    
    # Eu não gosto de aninhar funções para criar auxiliares, porém, como este código está
    # muito relacionado a esta abstração do arquivo, abrirei uma exceção.
    def print_formatado(nome, comprimento, tempo):
        "Função auxilar para formatar uma saída mais bonita, com os seguintes parâmetros necessários."
        lacuna = comprimento - len(nome)
        tabular = comprimento + lacuna
        SIMBOLO = '~ '
        
        print(f"{ESPACO}- {nome}{SIMBOLO:>{tabular}s}{traducao}")

    if len(LISTA_DE_CADASTROS) == 0:
        print("\nNão há cadastros.", end='\n\n')
    else:
        print(f"\nTodos os {total} abaixo:", end='\n\n')
        
        # Pega o comprimento do maior nome.
        comprimento = max(len(nome_cadastro(obj)) for obj in LISTA_DE_CADASTROS)
        # Espaço padrão para qualquer item listado.
        ESPACO = recuo(2)
        
        for dicio in LISTA_DE_CADASTROS:
            for nome in dicio:
                try:
                    antigo = dicio[nome]["criação"].timestamp()
                    novo = datetime.today().timestamp()
                    decorrido = novo - antigo
                    traducao = tempo_legivel(decorrido)
                    
                except ValueError:
                    SEM_VALOR = "(ERROR)"
                    traducao = SEM_VALOR
                    
                finally:
                    print_formatado(nome, comprimento, traducao)
        # Pula uma linha para ficar mais organizado(espaçado).
        print("")

def manual_de_ajuda_do_programa() -> None:
    print("""
        \rVocê pediu por ajuda. Aqui está o manual:

        \r\tAdicionar  - Realiza e adiciona novo cadastro.
        \r\tRemover    - Remove um cadastro do banco.
        \r\tAjuda      - Mostra este manual aqui.
        \r\tListar     - Listagem de cadastros realizados.
        \r\tInfo       - Mostra algumas estatísticas sobre o programa.
        \r\tSair       - Abandonar o programa de forma padrão. Lebrando que
        \r\t             outros métodos de fazer isso, não garante que os
        \r\t             cadastros removidos ou adicionados são salvos.
    """)

def cadastra_novo_usuario_agora() -> dict:
    "Realiza um cadastro agora, então envia o dicionário formado dele."
    nome = input(f"\n{recuo(4)}Nome do paciente: ")
    idade = int(input(f"{recuo(4)}Sua idade: "))
    nivel_de_dor = int(input(f"{recuo(4)}Nível de dor[1 à 5]: "))
    criacao = datetime.today()
    # Jeito de fazer clone da variável 'criação'.
    modificacao = criacao + timedelta(seconds=0)

    # Correção de uma entrada inválida.
    if nivel_de_dor > 5 or nivel_de_dor <= 0:
        print(f"Não aceito 'nível' igual á {nivel_de_dor}. Apenas valores de 1 à 5.")
        if nivel_de_dor > 5:
            nivel_de_dor = 5
        if nivel_de_dor < 0:
            nivel_de_dor = abs(nivel_de_dor) % 6
        if nivel_de_dor == 0:
            nivel_de_dor = 1
        print(f"O nível foi ajustado para {nivel_de_dor}.")

    return cria_cadastro(nome, idade, nivel_de_dor, criacao, modificacao)

def entrada_escolha_do_menu(menus: list[str]) -> int:
    "Pega uma lista com os menus, então retorna o número equivalente de cada opção."
    assert all(map(lambda item: isinstance(item, str), menus))
    
    entrada = entrada_pura_de_dados()
    print(barra_do_tamanho_da_tela('+'))

    if entrada.isdigit():
        valor = int(entrada)

        # Primeiro supõe que digitou o número:
        if 1 <= valor <= len(menus):
            return valor
        else:
            #raise IndexError(f"Não existe está opção {entrada}.")
            print(f"Numeração {entrada} não existe. Programa quebrou!")
            exit(2)
    elif entrada.isalpha():
        # Espera que há retorno.
        for (indice, opcao) in enumerate(menus):
            if entrada.lower() in opcao.lower():
                return (indice + 1)
        #raise ValueError(f"Não existe está opção {entrada}.")
        print(f"Não existe está opção '{entrada}'. Programa quebrou!")
        exit(2)
    else:
        #raise ValueError(f"Não aceita está entrada {entrada}, apenas 'int' e 'str'.")
        print (f"Não aceita está entrada {entrada}, apenas 'int' e 'str'. Programa quebrou!")
        exit(2)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Funções Auxiliares                                         #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
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

def cabecalho_padrao_do_hospital() -> None:
    "Cria o cabeçalho inicial do hospital em questão. Retorna nada."
    print(f"""
        \r{barra_do_tamanho_da_tela('=')}
           	\t\tCaadastrario dos Pacientes 
        		\t\tno
			{NOME_DO_HOSPITAL}
        \r{barra_do_tamanho_da_tela('=')}
        """)

def recuo(n: int) -> str:
    "Retorna string de recuo para dá margem a outras mensagens."
    ESPACO = ' '
    return ESPACO * n

def entrada_pura_de_dados() -> str:
    """
    Um simples prompt, entretanto, fica em loop se a entrada dada for uma
    string vázia, ou seja, o usuário apenas apertou ENTER direto.
    """
    entrada = input("Escolha uma opção: ")

    # Entradas vázias ficam apenas repetindo o comando.
    while entrada == '':
        entrada = input("Escolha uma opção: ")
    return entrada
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
from unittest import (TestCase)

class EntradaDeCadastroAgora(TestCase):
    def runTest(self):
        instancia = cadastra_novo_usuario_agora()

        pprint(instancia, indent='4')

class VisualizacaoDoMenu(TestCase):
    def setUp(self):
        self.MENU = ["Info", "Estatísticas", "Adicionar", "Deletar", "Obituário", "Listagem"]

    def runTest(self):
        visualizacao_do_menu(*self.MENU)

class EntradaEscolhaDoMenu(VisualizacaoDoMenu):
    def runTest(self):
        entrada = entrada_escolha_do_menu(self.MENU)

        print(f"Índice devolvido: {entrada}")
