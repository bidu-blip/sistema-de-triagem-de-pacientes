'''
    O objetivo do trabalho é fazer um sistema de triagem de pacientes. As instruções serão as seguintes:
  Usuário cadastra pacientes com nome, idade e nivel de dor (1 a 5). O programa exibe a lista ordenada
  pela gravidade.
'''
# Módulos pro próprio projeto:
from bancodedados import (
    adiciona_cadastro, carrega_banco_de_dados, salva_banco_de_dados, 
    todos_cadastros, busca_cadastro, remove_cadastro
    )
from interface import (
    cadastra_novo_usuario_agora, entrada_escolha_do_menu, visualizacao_do_menu, 
    listagem_de_cadastros, manual_de_ajuda_do_programa, cabecalho_padrao_do_hospital,
    mostra_distribuicao_de_gravidade, mostra_uma_info_mais_geral, 
    mostra_ultimos_e_primeiros_pacientes, alterna_ordenacao, atual_ordenacao
    )
from modelos import (nome_cadastro, mostra_cadastro)
from webpagina import (cria_pagina_com_cadastros)
# Biblioteca padrão do Python:
from pprint import (pprint as Pprint)
from sys import (argv as Argumentos)
import os
from unittest import (TestCase)

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                Execução do Programa
  Aqui fica a cópia do testes unitário 'PrototipoPrograma'. Toda vez que for modificado algo
lá, será copiado e colocado aqui.
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
"""
MENU_DE_OPCOES = [
    "Adicionar", "Remover", "Listar", "Info", "Consulta", 
    "Ordenação", "Ajuda", "Sair"
]


if __name__ == "__main__":
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
                    novo = cadastra_novo_usuario_agora()
                    try:
                        adiciona_cadastro(novo)
                    except NameError:
                        print("O nome já é cadastrado!")
                    finally:
                        pass
                case 2:
                    remove_paciente = input('\n\tNome do paciente à remover: ').strip()
                    texto_validacao = remove_paciente.replace(" ", '')
                    # Proposições(deste modo fica mais organizado):
                    E_UMA_STRING_VAZIA     = (remove_paciente == "")
                    CARACTERES_NAO_VALIDOS = (not texto_validacao.isalpha())
                    
                    if E_UMA_STRING_VAZIA or CARACTERES_NAO_VALIDOS:
                        print("Erro: Por favor, digite um nome válido contendo apenas letras.", end='\n\n')
                    else:
                        if remove_cadastro(remove_paciente):
                            print(f'\n\tPaciente {remove_paciente} removido com SUCESSO!', end='\n\n')
                        else:
                            print(f'\n\tO paciente \'{remove_paciente}\' não foi encontrado!', end='\n\n')
                case 3:
                    listagem_de_cadastros()
                    # Após uma listagem, também é alterado a página web também baseado nesta nova
                    # ordenação demanada.
                    cria_pagina_com_cadastros(todos_cadastros(), atual_ordenacao())
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
                    escolha = input("Alterar ordem prá: ")
                    alterna_ordenacao(escolha)
                    # Após mudança de ordem, altera a página web também baseado nesta nova
                    # ordenação demanada.
                    cria_pagina_com_cadastros(todos_cadastros(), atual_ordenacao())
                case 7:
                    manual_de_ajuda_do_programa()
                case 8:
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

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
class ProposicaoLogicaCorreta(TestCase):
    """
    Testa a lógica das proposições formadas para o prompt do nome que se consulta.
    """
    def runTest(self):
        def meuisalpha(texto) -> bool:
            for caractere in texto:
                if caractere.isalpha() or caractere.isspace():
                    pass
                else:
                    return False 
            return True
        
        remove_paciente = input('Digite o nome do paciente que deseja remover: ').strip()
        texto_validacao = remove_paciente
        # Preposições:
        E_UMA_STRING_VAZIA = (remove_paciente == "")
        #NAO_E_UM_TEXTO = (not texto_validacao.isalpha())
        NAO_E_UM_TEXTO = (not meuisalpha(texto_validacao))
        
        #self.assertTrue(remove_paciente == "" or not texto_validacao.isalpha())
        self.assertFalse(E_UMA_STRING_VAZIA or NAO_E_UM_TEXTO)
