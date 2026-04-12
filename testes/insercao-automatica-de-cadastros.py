"""
   Irá fazer inserção de cadastros de forma automatizada. É um teste integral, então 
 usa a inserção é a mais crua possível.
"""
from subprocess import (Popen, PIPE, DEVNULL)
from os import (popen)
from sys import (executable as CAMINHO_DO_INTERPLETADOR_PYTHON)
from pprint import (pprint)
from random import (choice, randint)
from datetime import (datetime, timedelta)
# Módulos da própria biblioteca:
from bancodedados import (
        adiciona_cadastro, 
        carrega_banco_de_dados, 
        salva_banco_de_dados
        )


def lista_de_nomes() -> list[str]:
    "Retorna uma liista de nomes, estes que estão no arquivo de amostra."
    CAMINHO_AOS_NOMES = "dados/testes/lista-de-nomes.txt"
    nomes_arquivo = open(CAMINHO_AOS_NOMES, "rt", encoding="utf8")
    conteudo = nomes_arquivo.read().split('\n')
    
    nomes_arquivo.close()
    return conteudo
    
def seleciona_nome_aleatorio(nomes: list[str]) -> str:
    "Seleciona um nome, na lista de nome, de forma randomica."
    return choice(nomes).rstrip('\n')

def datetime_aleatorio() -> datetime:
    "Cria um 'datetime' aleatório. O período da data em específico vária de 1980 à o ano atual."
    ANO_ATUAL = datetime.today().year 
    
    return datetime(
        hour=randint(0, 23),
        minute=randint(0, 59),
        second=randint(0, 59),
        # O hospital existe desde a década de 80.
        year=randint(1980, ANO_ATUAL),
        month=randint(1, 12),
        day=randint(1, 28)
    )

def cria_cadastro_aleatorio() -> dict:
    """
    Cria todo um cadastro de forma aleatórios, tanto o nome, idade, nível de dor e data 
    de criação, assim como as vezes, modificações também.
    """
    nome = seleciona_nome_aleatorio(lista_de_nomes())
    criacao = datetime_aleatorio()
    modificacao = criacao + timedelta(seconds=0)
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

def executa_programa_e_adiciona_um_cadastro_no_momento(cadastro: dict) -> None:
    # Extraindo partes específicas ...
    tupla       = list(cadastro.items())[0]
    nome        = tupla[0]
    outros      = tupla[1]
    idade       = outros["idade"]
    nivel       = outros["estado"]
    # Valores desnecessários para este tipo de inserção. Entretanto, ficará aqui
    # para dizer que, estamos reutilizando a função que gera o um cadastro 
    # aleatório.
    criacao     = outros["criação"]
    modificacao = outros["modificação"]
    # Criando lista de argumentos para a inserção seriada, onde é preciso
    # transformar em string e formatar algumas variáveis. Como mostrado acima,
    # nem todos valores dado pelo dício serão usados. Este tipo de inserção cria  os 
    # selos de tempo no momento.
    ARGUMENTOS_COM_QUEBRA_DE_LINHA = [
        b"adicionar\n", nome.encode(encoding='utf8') + b'\n',
        f"{idade}\n".encode(), 
        f"{nivel}\n".encode(), b"sair\n"
    ]
    processo = Popen(
        [CAMINHO_DO_INTERPLETADOR_PYTHON, "-B", "-OO", "main.py"],
        stdin=PIPE, stdout=DEVNULL
    )
    
    for valor in ARGUMENTOS_COM_QUEBRA_DE_LINHA:
        try:
            processo.stdin.write(valor)
            processo.stdin.flush()
        except EOFError:
            processo.stdin.writeline(valor)
            processo.stdin.flush()
            print("Foi inserido via 'comunicate'.")
        
    print("Cadastro abaixo inserido com sucesso de forma automática:")
    pprint(cadastro, indent=4)
   
def adiciona_um_cadastro_de_forma_direta(novo: dict) -> None:
    """
    Adiciona o cadastro dado, sem a execução do programa. Tratando diretamente com
    o banco de dados(arquivo JSON).
    """
    carrega_banco_de_dados()
    adiciona_cadastro(novo)
    salva_banco_de_dados() 
    print(f"""
          \rO cadastro abaixo foi adicionado com sucesso:
          \r\t{str(novo)}
          """)
    
if __name__ == "__main__":
    # Cria um cadastro agora, inserindo nome, idade e nível de dor apenas.
    #executa_programa_e_adiciona_um_cadastro_no_momento(cria_cadastro_aleatorio())
    #adiciona_um_cadastro_de_forma_direta(cria_cadastro_aleatorio())
    pass

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
from unittest import (TestCase, skip)
from time import (sleep)
@skip("Cuidado! Altera o arquivo JSON(banco de dados), insere um cadastro aleatório.")
class InsercaoAutomaticaDeCadastro(TestCase):
    def runTest(self):
        carrega_banco_de_dados()
        cadastro = cria_cadastro_aleatorio()
        
        pprint(cadastro)   
        adiciona_cadastro(cadastro)
        salva_banco_de_dados() 
        print("Cadastro realizado com sucesso.", end='\n\n')

class InsercoesAutomaticasEmSerie(TestCase):
    def runTest(self):
        X = randint(2, 5)
        amostras = [cria_cadastro_aleatorio() for _ in range(X)]
        cursor = 0
        PAUSA = 3.0
        
        print(f"Serão inseridas {X} ao total.")
        
        for cadastro in amostras:
            try:
                adiciona_um_cadastro_de_forma_direta(cadastro)
            except AttributeError as erro:
                print(cadastro)
                print(f"Falhou no {cursor + 1}! ({erro})")

            sleep(PAUSA)
            cursor += 1

class InsercaoDiretaManualComMecanismoAutomatico(TestCase):
    def runTest(self):
        adiciona_um_cadastro_de_forma_direta(cria_cadastro_aleatorio())
        adiciona_um_cadastro_de_forma_direta(cria_cadastro_aleatorio())
        
@skip("Alterar o banco de dados, alem de inserir a mesma entrada sempre!")           
class UmaInsercaoBasicaManualNoBanco(TestCase):
    def runTest(self):
        ARGUMENTOS = [b"Adicionar\n", 
                      "Mária Conceição Taváres\n".encode(encoding="utf8"),
                      "56\n".encode(), "1\n".encode()
                      ]
        handle = Popen(
            [CAMINHO_DO_INTERPLETADOR_PYTHON, "main.py"],
            stdin=PIPE, stdout=DEVNULL
        )
        
        for arg in ARGUMENTOS:
            handle.stdin.write(arg)
            handle.stdin.flush()
            argumento = arg.decode(encoding="utf8").strip('\n')
            print(f"Escrito argumento '{argumento}' com sucesso.")
        else:
            handle.stdin.write(b"sair\n")
        print("Um cadastro foi inserido com sucesso.")
