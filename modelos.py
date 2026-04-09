from datetime import (datetime, timedelta)
from unittest import (TestCase)

def cria_cadastro(nome: str, idade: int, nivel: int, criacao: datetime, modificacao: datetime) -> dict:
    "Cria uma instância do que será amarzenado no banco de dados no final."
    assert isinstance(nome, str)
    assert isinstance(idade, int)
    assert isinstance(nivel, int)
    assert isinstance(criacao, datetime)
    assert isinstance(modificacao, datetime)
    # Não podem referenciar o mesmo objeto.
    assert criacao is not modificacao

    return {
        nome: {
            "idade":       idade,
            "criação":     criacao,
            "modificação": modificacao,
            "estado":      nivel
          }
    }
