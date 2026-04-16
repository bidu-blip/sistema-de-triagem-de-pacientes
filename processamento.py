"""
  Funções de cunho totalmente de computar valores, e então retornar-los residirão
  neste módulo. Aqui ficam vários algoritmos que não geram saída de texto, e 
  apenas processam os dados obtidos. O arquivo comos os demais tem um amplo
  bem geral de processamento, e não funcionalidades específicas.
"""
# Biblioteca padrão do Python:
from unittest import (TestCase)
# Módulos pro próprio projeto:
from bancodedados import (
    adiciona_cadastro, carrega_banco_de_dados, salva_banco_de_dados, 
    todos_cadastros, busca_cadastro
    )
from modelos import (
    criacao_cadastro, 
    idade_cadastro, 
    nivel_de_dor_cadastro,
    maior_cadastro,
    cadastro_e_valido,
    nome_cadastro,
    traducao_do_nivel_de_dor
    )


def cadastro_mais_antigo_realizado() -> dict:
    "Encontra o paciente mais velho que frequentou aqui. Esteja ele vivo ou não."
    BANCO = todos_cadastros()
    TOTAL_DE_CADASTROS = len(BANCO)
    assert (TOTAL_DE_CADASTROS > 0)

    maximo = BANCO[0]

    for cadastro in BANCO[1:]:
        a = criacao_cadastro(maximo)
        b = criacao_cadastro(cadastro)

        if b > a:
            maximo = cadastro

    return maximo
        
def cadastro_mais_recente_realizado() -> dict:
    "Acha o paciente mais recente que chegou ao hospital."
    BANCO = todos_cadastros()
    TOTAL_DE_CADASTROS = len(BANCO)
    assert (TOTAL_DE_CADASTROS > 0)

    minimo = BANCO[0]

    for cadastro in BANCO[1:]:
        a = criacao_cadastro(minimo)
        b = criacao_cadastro(cadastro)

        if b < a:
            minimo = cadastro

    return minimo

def computa_a_distribuicao_da_triagem() -> dict:
    "Faz a divisão de frações do estado de cada paciente cadastrado no hospital."
    lista = todos_cadastros()
    distribuicao = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for cadastro in lista:
        indice = nivel_de_dor_cadastro(cadastro)
        distribuicao[indice] += 1
    
    total = sum(distribuicao.values())

    # Convertendo tudo em percentuais.
    for indice in range(1, 5 + 1):
        contagem = distribuicao[indice]
        distribuicao[indice] = contagem / total
    return distribuicao
      
def media_de_idade() -> int:
    "Calcula a média de idade dos pacientes cadastrados."
    lista_completa = todos_cadastros()
    quantidade = len(lista_completa)
    
    return int(sum(map(idade_cadastro, lista_completa)) / quantidade)

def ordena_cadastros_por_estado(lista: list[dict]) -> None:
    """
      Ordena uma lista de cadastros dada, do mais grave(parte de cima)
    para o mais leve(parte de baixo).
      O algoritmo usado abaixo é o 'select sort', que é um algoritmo
    de ordenação lento, porém bem intuitivo de criar.
    """
    # Apelido mais adequado para a função neste escopo.
    QUANTIA = len(lista)

    for i in range(QUANTIA - 1):
        # Posição na array de um suposto cadastro mais grave.
        maximo = i

        # Varrendo o resto da lista enquanto busca por um ainda 
        # pior.
        for j in range(i + 1, QUANTIA):
            pior = lista[maximo]
            outro = lista[j]

            # Se este 'cadastro' na iteração for mais grave que o já
            # registrado aqui, então marca a posição na lista.
            if maior_cadastro(outro, pior):
                maximo = j
        # Alterna os posições na lista.
        alterna_valores(lista, i, maximo)
    
def ordena_cadastros_por_nome(lista: list[dict]) -> None:
    """
      O algoritmo também ordena, igual a primeira(por estado), porém, o
    fator aqui é o nome, ou seja, por ordem alfabética, ao invés do 
    'estado de saúde' do paciente.
    """
    # Apelido mais adequado para a função neste escopo.
    QUANTIA = len(lista)

    for i in range(QUANTIA - 1):
        # Posição na array de um suposto cadastro mais grave.
        maximo = i

        # Varrendo o resto da lista enquanto busca por um ainda 
        # pior.
        for j in range(i + 1, QUANTIA):
            a = lista[maximo]
            b = lista[j]

            # Se este 'cadastro' na iteração for mais grave que o já
            # registrado aqui, então marca a posição na lista.
            if nome_precede(b, a):
                maximo = j
        # Alterna os posições na lista.
        alterna_valores(lista, i, maximo)
    
def ordena_cadastros_por_idade(lista: list[dict]) -> None:
    """
      O algoritmo também ordena, igual a primeira(por estado), porém, o
    fator aqui é a idade ao invés do 'estado de saúde' do paciente.
    """
    # Apelido mais adequado para a função neste escopo.
    QUANTIA = len(lista)

    for i in range(QUANTIA - 1):
        # Posição na array de um suposto cadastro mais grave.
        maximo = i

        # Varrendo o resto da lista enquanto busca por um ainda 
        # pior.
        for j in range(i + 1, QUANTIA):
            a = lista[maximo]
            b = lista[j]

            if idade_cadastro(b) >= idade_cadastro(a):
                maximo = j
        # Alterna os posições na lista.
        alterna_valores(lista, i, maximo)

def ordena_cadastros_por_criacao(lista: list[dict]) -> None:
    """
      O algoritmo também ordena, igual a primeira(por estado), porém, o
    fator aqui é a 'criação' ao invés do 'estado de saúde' do paciente.
    """
    # Apelido mais adequado para a função neste escopo.
    QUANTIA = len(lista)

    for i in range(QUANTIA - 1):
        # Posição na array de um suposto cadastro mais grave.
        maximo = i

        # Varrendo o resto da lista enquanto busca por um ainda 
        # pior.
        for j in range(i + 1, QUANTIA):
            a = lista[maximo]
            b = lista[j]

            if criacao_cadastro(b) > criacao_cadastro(a):
                maximo = j
        # Alterna os posições na lista.
        alterna_valores(lista, i, maximo)
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Funções Auxiliares                                         #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
def alterna_valores(lista: list[dict], q: int, p: int) -> None:
    "Realiza a troca de posições 'p' e 'q' na array 'lista'."
    auxiliar = lista[q]
    lista[q] = lista[p]
    lista[p] = auxiliar

def nome_precede(a: dict, b: dict) -> bool:
    "Verifica se o nome do cadastro[a] precede o cadastro[b]."
    assert cadastro_e_valido(a)
    assert cadastro_e_valido(b)

    # Faz uma comparação via nome das chaves dos dícios internos dos cadastros.
    return nome_cadastro(a) < nome_cadastro(b)
    
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
class OrdenacaoDeListaDeCadastros(TestCase):
    def listagem_dos_cadastros(self, lista):
        for item in lista:
            try:
                self.debug_cadastro(item)
            except:
                nome = nome_cadastro(item)
                print("Houve um erro com '{nome}'")
            finally:
                pass

    def debug_cadastro(self, cadastro):
        assert cadastro_e_valido(cadastro)

        nome = nome_cadastro(cadastro)
        estado = nivel_de_dor_cadastro(cadastro)
        estado = traducao_do_nivel_de_dor(estado)
        estado = estado.title()

        print(f"\t{nome:<40s}~ {estado}")

    def runTest(self):
        carrega_banco_de_dados() 

        amostra = todos_cadastros()

        print("Antes da alteração.")
        self.listagem_dos_cadastros(amostra)
        ordena_cadastros_por_estado(amostra)
        print("Depois da alteração.")
        self.listagem_dos_cadastros(amostra)
