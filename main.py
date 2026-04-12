'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada
  pela gravidade.
'''
# Módulos pro próprio projeto:
from bancodedados import (adiciona_cadastro, carrega_banco_de_dados, salva_banco_de_dados, todos_cadastros)
from interface import (
    cadastra_novo_usuario_agora, entrada_escolha_do_menu, visualizacao_do_menu, 
    listagem_de_cadastros, manual_de_ajuda_do_programa, cabecalho_padrao_do_hospital
    )
from modelos import (cria_cadastro, nome_cadastro, criacao_cadastro, mostra_cadastro)
# Biblioteca padrão do Python:
from pprint import (pprint as Pprint)

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                Execução do Programa
  Aqui fica a cópia do testes unitário 'PrototipoPrograma'. Toda vez que for modificado algo
lá, será copiado e colocado aqui.
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
MENU_DE_OPCOES = ["Adicionar", "Remover", "Listar", "Info", "Ajuda", "Sair"]

# Carrega todos os registros já feitos no banco de dados na memória.
carrega_banco_de_dados()
# Cabeçalho da abertura do programa.
cabecalho_padrao_do_hospital()

def cadastro_mais_antigo_realizado() -> dict:
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

while True:
    visualizacao_do_menu(*MENU_DE_OPCOES)
    
    try:
        match entrada_escolha_do_menu(MENU_DE_OPCOES):
            case 1:
                #adiciona_cadastro(entrada_de_cadastro_agora())
                novo = cadastra_novo_usuario_agora()
                adiciona_cadastro(novo)
                
            case 2:
                pass
            case 3:
                listagem_de_cadastros()
            case 4:
                total = len(todos_cadastros())
                antigo = cadastro_mais_antigo_realizado()
                recente = cadastro_mais_recente_realizado()

                print(f"\nO total de inserções é {total} cadastros.")
                print("Os cadastros mais velhos e novos feitos:")
                mostra_cadastro(antigo)
                mostra_cadastro(recente)

            case 5:
                manual_de_ajuda_do_programa()
            case 6:
                print("Você pressionou para sair.")
                break
            case _:
                print("Este número e oção não é válido.")
    except KeyboardInterrupt:
        print("Você apertou <Ctrl + C>, só será salvo que já foi adicionado.")
        break
    finally:
        pass
# Salva o que foi adicionado na lista da memória no banco de dados.    
salva_banco_de_dados()
