'''
   Função 'tempo' transforma o tempo em segundos(um decimal) para uma tradução
 mais legível de visualização. O retorno será uma string.
 
   Nota: Este arquivo foi retirado da minha conta GitHub pessoal. Este é o 
         endereço: https://github.com/patrick7star/python-utilitarios. Muito 
         do que jugo desnecessário foi excluído. Provavelmente o arquivo atende
         por outro nome. Nem tudo desnecessário foi excluído, portanto, deve
         haver algo que ainda fique.
'''
# o que será importado:
__all__ = ("tempo")

# Biblioteca padrão do Python:
from datetime import (datetime, timedelta)
from enum import (Enum, auto)
# Apelidos para algumas estruturas primitivas de retorno:
Decomposicao = {str: float, str:int, str:str}


# Constantes com escalas de tempo, com suas equivalências em segundos.
# A coisa dos múltiplos de submúltiplos são bem confusos, não seguem o
# sistema métrico... inicialmente!
minuto = 60
hora = 60 * minuto
dia =  24 * hora

# Nova notação disponível:
MILISEG  = 1e-3
MICROSEG = 1e-6
NANOSEG  = 1e-9
PICOSEG  = 1e-12
MINUTO   = 60
HORA     = hora
DIA      = dia
MES      = 30 * DIA
ANO      = 365 * DIA
# Bem aqui começa o sistema métrico...
DECADA   = 10 * ANO
SECULO   = 10 * DECADA
MILENIO  = 10 * SECULO

def tempo(segundos, arredonda=False, acronomo=False) -> str:
   "Faz um valor grande de tempo, dado puramente em segundos, mais legível."
   # Também aceita outros formatos de tempo reconhecidos em Python.
   if isinstance(segundos, timedelta):
      segundos = segundos.total_seconds()
   elif isinstance(segundos, datetime):
      agora = datetime.now()

      if segundos < agora:
         segundos = agora - segundos
      else:
         segundos = segundos - agora

      return tempo(segundos, arredonda, acronomo)

   # Fazendo a tradução normal.
   tempo_str = converte(segundos)
   # Deixa no singular se possível.
   tempo_str = transforma_no_singular(tempo_str)

   if acronomo and (not arredonda):
      return aplica_acronomo(tempo_str, False)
   elif (not acronomo) and arredonda:
      return arredonda_tempostr(tempo_str)
   elif  acronomo and arredonda:
      arredondado = arredonda_tempostr(tempo_str)
      return aplica_acronomo(arredondado, True)
   else:
      return tempo_str

def converte(t: float) -> str:
   """
     Representar o tempo de forma legível, onde converte todos valores
   passados na ordem de segundos para  minutos, horas décadas, meses,
   milisegundos, nanosegundos e etc...
   """
   # múltiplos e sub-múltiplos:
   if PICOSEG <= t < NANOSEG:
      grandeza = "picosegundos"
      return '%0.1f %s' % (t * 1.0e12, grandeza)
   elif NANOSEG <= t < MICROSEG:
      grandeza = 'nanosegundos'
      return '%0.1f %s' % (t * 1e9, grandeza)
   elif MICROSEG <= t < MILISEG:
      grandeza = 'microsegundos'
      return '%0.2f %s' % (t * 1e6, grandeza)
   elif MILISEG <= t < 1:
      grandeza = 'milisegundos'
      return '%0.2f %s' % (t * 1000, grandeza)
   elif 1 <= t < 60:
      grandeza = 'segundos'
      return '%0.2f %s' % (t, grandeza)
   elif t > 60 and t < 3600:
      grandeza = 'minutos'
      return '%0.2f %s' % (t / MINUTO, grandeza)
   elif t >= HORA and t < DIA:
      grandeza = 'horas'
      return '%0.2f %s' % (t / HORA, grandeza)
   elif t >= DIA and t < MES:
      return '%0.2f dias'%(t / DIA)
   elif t >= MES and t < ANO:
      return '%0.2f meses' % (t / MES)
   elif t >= ANO and t < DECADA:
      return '%0.2f anos' % (t / ANO)
   elif t >= DECADA and t < SECULO:
      grandeza = 'décadas'
      return '%0.2f %s' % (t / DECADA, grandeza)
   elif t >= SECULO and t < MILENIO:
      grandeza = 'séculos'
      return '%0.2f %s' % (t / SECULO, grandeza)
   elif t >= MILENIO and t < 10 * MILENIO:
      grandeza = 'milênios'
      return '%0.2f %s' % (t / MILENIO, grandeza)
   else:
      raise ValueError("não implementado para tal tamanho!")

def tempo_detalhado(t: str) -> str:
   """
   Decompõe uma string representando o tempo, e retorna uma nova com ele
   mais detalhado.
   """
   string = tempo(t)
   partes = decompoe(string)
   # apelido para simplificar codificação:
   peso = partes["peso"]

   if "minuto" in peso:
      tempo_seg = MINUTO * partes["fracao"]
      fracao_legivel = tempo(tempo_seg)
   elif "hora" in peso:
      tempo_seg = HORA * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "dia" in peso:
      tempo_seg = DIA * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "meses" in peso or "mês" in peso:
      tempo_seg = MES * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "ano" in peso:
      tempo_seg = ANO * partes["fracao"]
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "década" in peso:
      tempo_seg = DECADA * partes['fracao']
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "século" in peso:
      tempo_seg = SECULO * partes['fracao']
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   elif "milênio" in peso:
      tempo_seg = MILENIO * partes['fracao']
      fracao_legivel = tempo(tempo_seg, arredonda=True)
   else:
      raise Exception("não implementado para tal ainda!!")
   ...

   # retorno do tempo melhor detelhado.
   return (
      "{} {} {}"
      .format(
         partes["inteiro"],
         partes["peso"],
         fracao_legivel
      )
   )

def decompoe(tempo_str: str) -> Decomposicao:
   "Decompõe em partes a 'string de tempo'."
   partes = tempo_str.split()
   peso = partes.pop()
   valor = partes.pop()
   # Objeto desnecessário, acabando com sua vida neste momento, sem 
   # qualquer chance para o GB fazer-lô automaticamente.
   del partes

   try:
      (inteiro, fracao) = valor.split('.')
      fracao = float('0.' + fracao)
      inteiro = int(inteiro)
   except ValueError:
      fracao = 0
      inteiro = int(valor)
   else:
      pass

   return {
      'fracao': fracao,
      'inteiro': inteiro,
      'peso': peso
   }

def arredonda_tempostr(tempo_str) -> str:
   "Pega uma 'conversão' e arredonda sua parte inteira."
   partes = decompoe(tempo_str)
   inteiro = partes['inteiro']
   fracao = partes['fracao']
   peso = partes['peso']

   if fracao > 0.5:
      inteiro += 1

   return "{} {}".format(inteiro, peso)

def aplica_acronomo(tempo_str: str, arredonda: bool) -> str:
   "Pega uma string já em forma legível e encurta seu acrônomo. "
   partes = decompoe(tempo_str)
   (i, f, peso) = (
      partes['inteiro'],
      partes['fracao'],
      partes['peso']
   )
   encostado = False

   if "picosegundo" in peso:
      peso = "ps"
      encostado = True
   elif 'nanosegundo' in peso:
      peso = 'ns'
      encostado = True
   elif "microsegundo" in peso:
      peso = "μs"
      encostado = True
   elif "milisegundo" in peso:
      peso = "ms"
      encostado = True
   elif "segundo" in peso:
      peso = "seg"
   elif "minuto" in peso:
      peso = "min"
   elif "hora" in peso:
      peso = "h"
      encostado = True
   elif "década" in peso:
      peso = 'déc'
   elif "milênio" in peso:
      peso = 'mil'
   ...

   valor = i + f
   espaco = ' '
   if encostado:
      espaco = ''
   if arredonda and f == 0.0:
      return "%i%s%s" % (int(valor), espaco, peso)
   else:
      return "%0.2f%s%s" % (valor, espaco, peso)

def transforma_no_singular(tempo_str) -> str:
   "Transforma 'tempo_str' na forma singular, se este for o caso."
   # verificando se é o caso que estamos querendo consertar.
   partes = decompoe(tempo_str)
   e_caso_procurado = (
      partes['inteiro'] == 1 and
      partes['fracao'] == 0.0
   )

   if e_caso_procurado:
      # transforma no valor novamente ...
      valor = partes['inteiro'] + partes['fracao']
      # remove o plural.
      tamanho = len(partes['peso'])
      peso = partes['peso'][0:tamanho-1]
      # retornando o valor dirigido no singular.
      return "{} {}" .format(valor, peso)
   else:
      # não é o caso, apenas devolve dado.
      return tempo_str
   ...

# == == == == == == == == == == == === == == == == == == == == == == == ===
#                             Valores Grandes
# == == == == == == == == == == == === == == == == == == == == == == == ===
def valor_grande_legivel(numero: int) -> str:
   if numero >= 1_000 and numero < 1_000_000:
      return "{:0.1f} mil".format(numero / 1_000)
   elif  pow(10, 6) <= numero < pow(10, 9):
      return "{:0.1f} mi".format(numero / pow(10, 6))
   elif pow(10, 9) <= numero < pow(10, 12):
      return "{:0.1f} bi".format(numero / pow(10, 9))
   elif pow(10, 12) <= numero < pow(10, 15):
      return "{:0.1f} ti".format(numero / pow(10, 9))
   else:
      return str(numero)
...

def valor_grande_bem_formatado(numero: int) -> str:
   if numero < 1000:
      return str(numero)
   else:
      forma_inicial = str(numero)
      resto = len(forma_inicial) % 3
      forma_inicial = ''.join(['0'*(3 - resto), forma_inicial])
      # fila para armazenar caractéres temporiamente,
      # e string para concatenação.
      fila = []; numero_str = ""

      for c in list(forma_inicial):
         fila.append(c)
         # deseja numa classe a formação dos três algs.
         if len(fila) == 3:
            numero_str += ' '
            while len(fila) > 0:
               numero_str += fila.pop(0)
         ...
      ...
      numero_str += ' '
      while len(fila) > 0:
         numero_str += fila.pop(0)
      return numero_str.lstrip('0 ')
   ...
...
