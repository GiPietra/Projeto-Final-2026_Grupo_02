# Funções de manipulação de sequências de DNA.
#
# Nossa "mini BioPython"! Aqui cada função recebe uma sequência como uma
# STRING (ex: "ATCG") e devolve um resultado (outra string, um número, etc.).
#
# IMPORTANTE: implemente cada função abaixo. Apague o
# "raise NotImplementedError(...)" quando for resolver.

# Você vai precisar destas constantes
from bio.constantes import DNA_PARA_AMINOACIDO, DNA_STOP_CODONS, CONVERSOR_DE_BASE


def complementar(sequencia):
    """
    Retorna uma NOVA string com a sequência complementar.

    Lembre-se do pareamento das bases: A<->T e C<->G.
    Ex: complementar("ATCG") -> "TAGC"

    Dica: percorra cada base da sequência e vá montando (concatenando)
    a sequência complementar numa nova string.
    """
    seq_complementar = ""

    for base in sequencia:
        seq_complementar += CONVERSOR_DE_BASE[base]
    return seq_complementar


def complementar_reversa(sequencia):
    """
    Retorna uma NOVA string com a sequência complementar reversa.

    Ex: complementar_reversa("ATCG") -> "CGAT"

    Dica: é o complementar "de trás para frente". Você pode reaproveitar
    a função complementar() que acabou de escrever e depois inverter o
    resultado (lembre-se do truque de fatiamento [::-1]).
    """
    raise NotImplementedError("Implemente a função complementar_reversa")


def transcrever(sequencia):
    """
    Retorna uma NOVA string com o resultado da transcrição (DNA -> RNA).

    Ex: transcrever("ATCG") -> "AUCG"

    Dica: na transcrição, a base T (timina) vira U (uracila).
    """
    raise NotImplementedError("Implemente a função transcrever")



def calcular_percentual(sequencia, lista_bases):
    """
    Recebe uma LISTA de bases e retorna o percentual dessas bases na sequência.

    Ex: calcular_percentual("ATCGAAA", ["A"]) -> 0.5   (4 As em 8 bases... veja abaixo)
    Ex: calcular_percentual("ATCGCC", ["C", "G"]) -> ~0.66  (4 Cs/Gs em 6 bases)

    Dica: conte quantas bases da sequência estão dentro da lista "bases" e
    divida pelo tamanho total da sequência.
    """
    raise NotImplementedError("Implemente a função calcular_percentual")
    

def calcular_percentual_gc(sequencia):
    """
    Retorna o percentual de G e C na sequência (conteúdo GC).

    Ex: calcular_percentual_gc("ATCGCC") -> ~0.66

    É a mesma coisa que calcular_percentual(sequencia, ["G", "C"]), só que
    já vem pronta com as bases "G" e "C", assim dá pra usar direto com
    df["sequencia"].apply(calcular_percentual_gc), sem precisar de lambda.
    """
    base_count_list = 0
    for base in sequencia:
        if base == "G":
            base_count_list += 1
        elif base == "C":
            base_count_list += 1
    
    list_base_percentage = (base_count_list/len(sequencia))
    return list_base_percentage



def contar_bases(sequencia):
    """
    Retorna um DICIONÁRIO com a contagem de cada base na sequência.

    Ex: contar_bases("ATCGA") -> {"A": 2, "T": 1, "C": 1, "G": 1}

    Dica: crie um dicionário começando as contagens em 0 e vá somando 1
    conforme percorre cada base da sequência. (Isso vai ser bem útil no
    exercício de pandas!)
    """
    raise NotImplementedError("Implemente a função contar_bases")


def encontrar_inicio(sequencia):
    """
    Retorna a sequência a partir do primeiro START CODON (o códon "ATG").

    O ATG é onde a tradução de um gene começa (ele também codifica o primeiro
    aminoácido, a metionina "M"). Antes dele costuma haver uma região que não
    é traduzida, então, para achar a proteína, primeiro precisamos "pular" até
    esse início.

    Ex: encontrar_inicio("CCATGGGGTAA") -> "ATGGGGTAA"
    Se não houver nenhum "ATG", retorne uma string vazia "".

    Depois, é só traduzir o resultado:
        traduzir(encontrar_inicio(sequencia), parar=True)

    Dica: as strings têm um método .find("ATG") que devolve a posição do
    primeiro "ATG" (ou -1 se não encontrar). A partir daí, use fatiamento.
    """
    seq_inicio = ""

    for num in range(sequencia.find("ATG"),len(sequencia)):
        seq_inicio += sequencia[num]
    return seq_inicio


def traduzir(sequencia, parar=False):
    """
    Retorna uma STRING com a tradução da sequência para uma proteína.

    Ex: traduzir("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG") -> "MAIVMGR*KGAR*"

    Regras:
    - Não precisa achar o código de ínicio! Parta do presuposto que sua função já recebe
    uma sequencia q inicia com códon ATG.
    - Leia a sequência de 3 em 3 bases (cada trinca é um "códon").
    - Use o dicionário DNA_PARA_AMINOACIDO (em bio/constantes.py) para
      descobrir qual aminoácido cada códon representa.
    - Se o códon for um stop codon (veja a lista DNA_STOP_CODONS), o
      aminoácido é "*".
    - Se a trinca NÃO estiver no dicionário (base indefinida, como "N"),
      use "X" para indicar que não dá para saber.
    - Se parar=True, a tradução deve PARAR no primeiro stop codon.
      Se parar=False, continue até o fim, marcando os stops como "*".

    Dica: importe o dicionário no topo do arquivo:
        from bio.constantes import DNA_PARA_AMINOACIDO, DNA_STOP_CODONS
    Dica: para pegar as trincas, o passo do range pode ser 3 -> range(0, len, 3).
    """
    raise NotImplementedError("Implemente a função traduzir")