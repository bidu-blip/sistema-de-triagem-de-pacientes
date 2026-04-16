"""
   Script gera uma página HTML baseado em todos os cadastros contidos no
 banco de dados.
"""
from unittest import (TestCase)
from random import (choice)
from bancodedados import (carrega_banco_de_dados, todos_cadastros, )
from interface import (NOME_DO_HOSPITAL)
from modelos import (traducao_do_nivel_de_dor, nome_cadastro, idade_cadastro,
                     nivel_de_dor_cadastro, cadastro_e_valido,
                     criacao_cadastro)


# Como esta parte é meio que estática, pode ser definida na inicialização. Viram simples
# constantes no programa. Nenhuma formatação é feita, simples trechos copiados dos
# e ligados a variáveis(como dissoe, constantes).
COMENTARIO_DA_PAGINA = """
<!--
  Prompt que foi necessário para gerar, ao menos o básico desta página, com o
  Gemini:

  Por favor, gere uma simples página que mostre um título no formato daqueles
  de jornais, este separado por uma barra. Abaixo disso tudo vem uma tabela,
  com os campos necessários do sistema de triagem: nome, idade, nível de dor,
  criação. O esquema de cores que estou pensando é, algo parecido com o GitHub
  no modo 'dark'. Eu quero as bordas da tabelas bem amigaveis,... bem
  redondas. O código tem que ser apenas em HTML puro, nada de CSS ou
  JavaScript. Também, tente espaçar cada parte importante. Não tenho muito
  conhecimento dele assim para diferenciar tudo.
 -->
"""
TITULO_DA_PAGINA = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{NOME_DO_HOSPITAL}</title>
</head>
"""
CABECALHO_DA_PAGINA = f"""
    <h1 align="center" style="color: #5ec1df; font-family: 'Times New Roman', serif; letter-spacing: 2px;">
        {NOME_DO_HOSPITAL}
    </h1>
    <hr size="2" color="#30363d" width="90%">
    <br>
"""
CONFIGURACAO_DO_CORPO = """
<body text="#c9d1d9" bgcolor="#0d1117" style="font-family: Arial, sans-serif; padding: 20px;">
"""
TAGS_FINAIS = "</body>\n</html>\n"


def cor_especifica_para_nivel_de_dor(nivel: int) -> str:
   "Seleciona uma cor baseado no estado de saúde do paciente(de 1 à 5)."
    assert isinstance(nivel, int)

    match nivel:
        case 5:
            #return "#f50000"
            return "#fc4b7d"
        case 4:
            #return "#c4006f"
            return "#ef7fe4"
        case 3:
            #return "#f5b700"
            return "#fcf767"
        case 2:
            #return '#03559e'
            return "#74affc"
        case 1:
            #return "#6ed900"
            return "#74fc76"
        case _:
            raise ValueError("Não existe este nível!")

def cria_linha_da_tabela(cadastro: dict, paleta:str = None) -> str:
    "Seleciona cor baseado no nível de gravidade para coloração do texto na página."
    assert cadastro_e_valido(cadastro)

    NOME_DO_PACIENTE = nome_cadastro(cadastro)
    SUA_IDADE = idade_cadastro(cadastro)
    NIVEL = nivel_de_dor_cadastro(cadastro)
    ESTADO_DE_SAUDE = traducao_do_nivel_de_dor(NIVEL).title()
    DATA_DE_ENTRADA = criacao_cadastro(cadastro).strftime("%d/%m/%Y às %I %p")
    COR = cor_especifica_para_nivel_de_dor(NIVEL)

    if paleta is None:
        return f"""
        \r        <tr>
        \r            <td><b>{NOME_DO_PACIENTE}</b></td>
        \r            <td align="center">{SUA_IDADE}</td>
        \r            <td style='color:{COR}'><b>{ESTADO_DE_SAUDE}</b></td>
        \r            <td>{DATA_DE_ENTRADA}</td>
        \r        </tr>
            """
    else:
        return f"""
        \r        <tr bgcolor="{paleta}">
        \r            <td><b>{NOME_DO_PACIENTE}</b></td>
        \r            <td align="center">{SUA_IDADE}</td>
        \r            <td style='color:{COR}'><b>{ESTADO_DE_SAUDE}</b></td>
        \r            <td>{DATA_DE_ENTRADA}</td>
        \r        </tr>
            """

def transforma_cadastros_em_linhas_de_tabela(lista: list[dict]) -> str:
    CONFIGURACAO_DA_TABELA = """
        <table align="center" width="90%" cellpadding="15" cellspacing="0" style="background-color: #161b22; border-radius: 12px; overflow: hidden; border: 1px solid #30363d;">
    """
    LINHA_DE_LEGENDAS_DA_TABELA = """
        <tr bgcolor="#21262d" style="text-align: left; font-size: 18px; color: #ffffff;">
            <th width="10%">Nome</th>
            <th width="20%", align="center">Idade</th>
            <th width="25%">Estado do Paciente</th>
            <th width="15%">Entrada</th>
        </tr>
    """
    cursor = 0
    PALETAS = ["#161b22", "#0d1117",]
    linhas = []

    # Iterando e transformando cada cadastro na seguinte linha em HTML.
    for cadastro in lista:
        paleta = PALETAS[cursor % 2]
        transformacao = cria_linha_da_tabela(cadastro, paleta)
        linhas.append(transformacao)
        cursor += 1
    # Concatena todos os "parsers" realizados.
    LINHAS = "\n".join(linhas)

    # A tabulação tem que ficar neste bem assim, então o arquivo gerado
    # seguirar o original do site. Foram feitas copias exatamente assim
    # do original.
    return f"""
       \r{CONFIGURACAO_DA_TABELA}
       \r    {LINHA_DE_LEGENDAS_DA_TABELA}
       \r    {LINHAS}
       \r    </table>
    """

if __name__ == "__main__":
    carrega_banco_de_dados()
    lista_bd = todos_cadastros()

    print("A criação da página ...", end=' ')
    transformacao = "".join([
        COMENTARIO_DA_PAGINA,
        TITULO_DA_PAGINA,
        CABECALHO_DA_PAGINA,
        CONFIGURACAO_DO_CORPO,
        transforma_cadastros_em_linhas_de_tabela(lista_bd),
        TAGS_FINAIS
    ])
    print("foi concluida com sucesso.")

    arquivo = open("site-visualizador.html", "wt")
    print(transformacao, file=arquivo)
    arquivo.close()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
class PrototipoDeGeracaoDaPagina(TestCase):
    def runTest(self):
        carrega_banco_de_dados()
        lista_bd = todos_cadastros()
        transformacao = "".join([
            COMENTARIO_DA_PAGINA,
            TITULO_DA_PAGINA,
            CABECALHO_DA_PAGINA,
            CONFIGURACAO_DO_CORPO,
            transforma_cadastros_em_linhas_de_tabela(lista_bd),
            TAGS_FINAIS
        ])
        print(transformacao)

class CriandoLinhaPraTabelaComCadastro(TestCase):
    def runTest(self):
        carrega_banco_de_dados()

        lista = todos_cadastros()
        escolha = choice(lista)

        print(cria_linha_da_tabela(escolha))

class ParsearBDPraLinhasDeTabelas(TestCase):
    def runTest(self):
        carrega_banco_de_dados()

        lista = todos_cadastros()
        funcao = transforma_cadastros_em_linhas_de_tabela
        resultado = funcao(lista)

        print(resultado)
