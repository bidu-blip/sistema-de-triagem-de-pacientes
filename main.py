'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada
  pela gravidade.
'''
# Módulos pro próprio projeto:
from bancodedados import (
    adiciona_cadastro, carrega_banco_de_dados, salva_banco_de_dados, 
    todos_cadastros, busca_cadastro
    )
from interface import (
    cadastra_novo_usuario_agora, entrada_escolha_do_menu, visualizacao_do_menu, 
    listagem_de_cadastros, manual_de_ajuda_do_programa, cabecalho_padrao_do_hospital
    )
from modelos import (cria_cadastro, nome_cadastro, criacao_cadastro, mostra_cadastro, 
                     nivel_de_dor_cadastro, traducao_do_nivel_de_dor, idade_cadastro)
# Biblioteca padrão do Python:
from pprint import (pprint as Pprint)
from sys import (argv as Argumentos)
import os

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                Execução do Programa
  Aqui fica a cópia do testes unitário 'PrototipoPrograma'. Toda vez que for modificado algo
lá, será copiado e colocado aqui.
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
MENU_DE_OPCOES = [
    "Adicionar", "Remover", "Listar", "Info","Consulta", 
    "Ajuda", "Sair"
]


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

def computa_a_distribuicao_da_triagem() -> dict:
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
    lista_completa = todos_cadastros()
    quantidade = len(lista_completa)
    
    return int(sum(map(idade_cadastro, lista_completa)) / quantidade)

def mostra_distribuicao_de_gravidade():
    distribuicao = computa_a_distribuicao_da_triagem()
    
    print("\nComo estão dividido a triagem dos pacientes cadastros:")
    
    for (tipo, percentual) in distribuicao.items():
        estado = traducao_do_nivel_de_dor(tipo)
        
        print(f"\t{estado.capitalize():<20s} ~{percentual * 100.0:0.1f}%")

def mostra_uma_info_mais_geral():
    total = len(todos_cadastros())
    
    print(f"\nO total de inserções é {total} cadastros.")
    print(f"A média de idade é {media_de_idade()} anos.")
    print("\nOs cadastros mais velhos e novos feitos:")

def mostra_ultimos_e_primeiros_pacientes():
    antigo = cadastro_mais_antigo_realizado()
    recente = cadastro_mais_recente_realizado()
    
    mostra_cadastro(antigo)
    mostra_cadastro(recente)

# Carrega todos os registros já feitos no banco de dados na memória.
carrega_banco_de_dados()
# Cabeçalho da abertura do programa.
cabecalho_padrao_do_hospital()

# Laço infinito, assim fica pedindo o que o usuário deseja executar nele.
while True:
    # Mostra o menu se não a primeira vez, então novamente. 
    visualizacao_do_menu(*MENU_DE_OPCOES)
    
    # Captura terminos repetinos como o sinal de <Ctrl + C>, permitindo assim,
    # salvar cadastros alterados, inseridos ou removidos.
    try:
        match entrada_escolha_do_menu(MENU_DE_OPCOES):
            case 1:
                #adiciona_cadastro(entrada_de_cadastro_agora())
                novo = cadastra_novo_usuario_agora()
                try:
                    adiciona_cadastro(novo)
                except NameError:
                    print("O nome já é cadastrado!")
                finally:
                    pass
            case 2:
                remove_paciente = input('Digite o nome do paciente que deseja remover: ').strip()
                texto_validacao = remove_paciente
                
                if remove_paciente == "" or not texto_validacao.isalpha():
                    print("Erro: Por favor, digite um nome válido contendo apenas letras.")
                else:
                    if remove_cadastro(remove_paciente):
                        print(f'Paciente {remove_paciente} removido com SUCESSO!')
                    else:
                        print(f'O paciente \'{remove_paciente}\' não foi encontrado!')
            case 3:
                listagem_de_cadastros()
            case 4:
                mostra_uma_info_mais_geral()
                mostra_ultimos_e_primeiros_pacientes()
                mostra_distribuicao_de_gravidade()
                # Espaçador de linha.
                print("")

            case 5:
                prompt = input("\nDigite o nome completo: ")
                resultado = busca_cadastro(prompt)

                if resultado is not None and isinstance(resultado, dict):
                    mostra_cadastro(resultado)
                elif isinstance(resultado, list):
                    print("\nNome dado é ambíguo. Aqui estão algumas opções:", end='\n\n')

                    for item in resultado:
                        print(f'\t- {nome_cadastro(item)}')
                    print("\n")

                else:
                    print(f"Não foi encontrado o nome '{prompt}'. Absolutamente nada!")
            case 6:
                manual_de_ajuda_do_programa()
            case 7:
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
