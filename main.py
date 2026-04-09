'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada
  pela gravidade.
'''
from bancodedados import (adiciona_cadastro, carrega_banco_de_dados, salva_banco_de_dados)
from interface import (
    cadastra_novo_usuario_agora, entrada_escolha_do_menu, visualizacao_do_menu, 
    listagem_de_cadastros, manual_de_ajuda_do_programa, cabecalho_padrao_do_hospital
    )
from modelos import (cria_cadastro)

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                Execução do Programa
  Aqui fica a cópia do testes unitário 'PrototipoPrograma'. Toda vez que for modificado algo
lá, será copiado e colocado aqui.
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
MENU_DE_OPCOES = ["Adicionar", "Remover", "Listar", "Ajuda", "Sair"]

carrega_banco_de_dados()
cabecalho_padrao_do_hospital()

while True:
    visualizacao_do_menu(*MENU_DE_OPCOES)
    
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
            manual_de_ajuda_do_programa()
        case 5:
            print("Você pressionou para sair.")
            break
        case _:
            print("Este número e oção não é válido.")

salva_banco_de_dados()
