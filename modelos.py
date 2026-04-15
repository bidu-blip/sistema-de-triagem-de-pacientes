# Biblioteca padrão do Python:
from datetime import (datetime, timedelta)
from unittest import (TestCase)
from pprint import (pprint as PPrint)
# Módulos pro próprio projeto:

def cadastro_e_valido(cadastro: dict) -> bool:
    """
    Como o cadastro é um dicionário, e o polimorfismo do Python aceita qualquer coisa
    esta função cuida de validar apenas dicionário que representam um cadastro de fato.
    """
    # Atribuição da chave nome, supostamente a única chave no dicionário passado.
    for chave in cadastro:
        nome = chave

    CHAVES = cadastro[nome].keys()
    subdicio = cadastro[nome]
    # Há uma chave(o nome), e quatro chave-valor no dicionário desta chave.
    sem_excesso = (len(subdicio) == 4 and len(cadastro) == 1)
    
    if (not sem_excesso):
        return False
    
    tem_todos_campos = (
        # Verifica se há as chaves específicas aqui.
        "idade"        in CHAVES  and
        "estado"       in CHAVES  and
        "criação"      in CHAVES  and
        "modificação"  in CHAVES
    )
    sao_dos_tipos_correspondentes = (
        # Elas são dos tipos atestados. 
        isinstance(subdicio["idade"], int)              and
        isinstance(subdicio["estado"], int)             and
        isinstance(subdicio["criação"], datetime)       and
        isinstance(subdicio["modificação"], datetime)   
    )
    
    
    return tem_todos_campos and sao_dos_tipos_correspondentes

def cria_cadastro(nome: str, idade: int, nivel: int, criacao: datetime, modificacao: datetime) -> dict:
    "Cria uma instância do que será amarzenado no banco de dados no final."
    assert isinstance(nome, str)
    assert isinstance(idade, int)
    assert isinstance(nivel, int)
    assert isinstance(criacao, datetime)
    assert isinstance(modificacao, datetime)
    # Não podem referenciar o mesmo objeto.
    assert criacao is not modificacao

    # Retorna um dicionário, sendo este tendo uma única chave 'nome', e valor 
    # desta chave será um dicionário com cinco campos(talvez mais no futuro),
    # bem definidos.
    return {
        nome: {
            "idade":       idade,
            "criação":     criacao,
            "modificação": modificacao,
            "estado":      nivel
          }
    }

# Operadores lógicos do cadastro em termos de funções.
def igualdade_cadastro(a: dict, b: dict) -> bool:
    """
    Verifica se os cadastros 'a' e 'b' são iguais, nos termos deste programa, 
    obviamente. Eles só serão iguais se, e somente se, os nomes forem iguais
    e o tempo de criação entre eles for de um dia à uma semana.
    """
    assert cadastro_e_valido(a)
    assert cadastro_e_valido(b)

    diferenca = criacao_cadastro(a) - criacao_cadastro(b)
    return diferenca < timedelta(weeks=1)

# Metodos para consulta dos campos do 'Cadastro'. Como o tipo de dado abstrado
# não é uma 'classe', estes 'métodos' não são ligados ao objeto.
def nome_cadastro(cadastro: dict) -> str:
    """
    Retorna o nome do cadastro dado. Parece bastante trivial para cá, mas é 
    bom lembrar que, o cadastro é um aninhamento de dicionários, portanto seu 
    nome não é tão fácil de acessar quanto parece.
    """
    assert cadastro_e_valido(cadastro)

    for nome in cadastro:
        return nome

def criacao_cadastro(cadastro: dict) -> datetime:
    "Retorna a data de criação do cadastro no sistema."
    assert cadastro_e_valido(cadastro)

    return cadastro[nome_cadastro(cadastro)]["criação"]

def idade_cadastro(cadastro: dict) -> int:
    "Retorna a idade do cadastro dado."
    assert cadastro_e_valido(cadastro)

    return cadastro[nome_cadastro(cadastro)]["idade"]

def nivel_de_dor_cadastro(cadastro: dict) -> int:
    "Retorna o nível de dor do cadastro dado."
    assert cadastro_e_valido(cadastro)

    return cadastro[nome_cadastro(cadastro)]["estado"]

# Outros métodos relacionados a este tipo de dado.
def mostra_cadastro(cadastro: dict) -> None:
    "Recursos importantes do cadastro dado. E também melhores interpretados."
    assert cadastro_e_valido(cadastro)

    OUTRO_RECUO = ' ' * 3
    RECUO = ' ' * 5
    nome = nome_cadastro(cadastro)
    idade = idade_cadastro(cadastro)
    nivel = nivel_de_dor_cadastro(cadastro)
    nivel = traducao_do_nivel_de_dor(nivel).capitalize()
    data = cadastro[nome]["criação"]
    datastr = data.strftime("%d/%m/%Y às %I%p")
    # Já é sabido qual o maior rótulo.
    maior = len("Nível de dor")

    print(
        f"""
        \r{OUTRO_RECUO}{nome}
        \r{RECUO}- Nível de dor {nivel:.>29s}
        \r{RECUO}- Idade {idade:.>29d}
        \r{RECUO}- Entrada {datastr:.>29s}
        """, 
    )

def traducao_do_nivel_de_dor(nivel: int) -> str:
    "Retorna um texto mais legível para os inteiros relacionados a níveis de dor."
    assert isinstance(nivel, int)
    assert 1 <= nivel <= 5

    match nivel:
        case 1:
            return "sem gravidade"
        case 2:
            return "leve"
        case 3:
            return "monitorado"
        case 4:
            return "grave"
        case 5:
            return "muito grave"

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
#                                Testes Unitários                                           #
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --#
class ValidadeDeUmCadastro(TestCase):
    def runTest(self):
        hoje = datetime.today()
        entradas = [
            {
                "André Marcos": {
                    "idade": 15,
                    "criação": hoje - timedelta(hours=5, days=7),
                    "modificação": hoje - timedelta(hours=3),
                    "estado": 3
                }
            },
            # Tem um campo a mais no sub-dicionário.
            {
                "Júlia Marques Ducá": {
                    "não-existe": "nada",
                    "idade": 55,
                    "criação": hoje - timedelta(hours=3, days=1),
                    "modificação": hoje - timedelta(hours=2),
                    "estado": 4
                }
            },
            # Tem uma chave a mais no dicionário.
            {
                "André Leão Albuquerque": {
                    "idade": 2,
                    "criação": hoje - timedelta(hours=13, days=12),
                    "modificação": hoje - timedelta(hours=12),
                    "estado": 1
                },
                "Preferências": {
                    "fruta": "Morango",
                    "objeto": "Caneta"
                }
            },
            {
                "André Leão Albuquerque": {
                    "idade": 2,
                    "criação": hoje - timedelta(hours=13, days=12),
                    "modificação": hoje - timedelta(hours=12),
                    "estado": 1
                },
                "Cor": "Branca"
            },
        ]
        
        PPrint(entradas)
        self.assertTrue(cadastro_e_valido(entradas[0]))
        self.assertFalse(cadastro_e_valido(entradas[1]))
        self.assertFalse(cadastro_e_valido(entradas[2]))
        self.assertFalse(cadastro_e_valido(entradas[3]))
