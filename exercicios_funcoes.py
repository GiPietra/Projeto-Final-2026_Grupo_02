# Exercícios das funções
#
# Aqui você testa CADA função que criou em bio/sequencia.py, isoladamente,
# numa sequência pequena, para conferir que todas funcionam.
#
# Leia o enunciado no README (seção "Exercícios das funções").
#
# Para cada bloco abaixo, escreva um print mostrando o resultado e confira se
# bate com o esperado no comentário.

from bio.sequencia import (
    complementar,
    complementar_reversa,
    transcrever,
    traduzir,
    calcular_percentual,
    calcular_percentual_gc,
    contar_bases,
    encontrar_inicio,
)


# 1) complementar        — esperado: "TAGC"

print(f"Resultado da função complementar:{complementar("ATCG")}")

# 2) complementar_reversa — esperado: "CGAT"
print(complementar_reversa("ATCG"))


# 3) transcrever          — esperado: "AUCG"
print(f"Resultado da função transcrever:{transcrever("ATCG")}")


# 4) encontrar_inicio     — esperado: "ATGGGGTAA" (começa no 1º ATG)

print(f"Resultado da função encontrar início: {encontrar_inicio("CCCATGGGGTAA")}")


# 5) traduzir             — esperado: "MAIVMGR*KGAR*"
print(traduzir("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"))

#    traduzir com parar=True — deve PARAR no primeiro stop codon, esperado: "MAIVMGR"
print(traduzir("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", parar=True))


# 6) calcular_percentual  — esperado: 0.5 (metade das bases é A)
print(calcular_percentual("ATCGAAAA", ["A"]))

# 7) calcular_percentual_gc — esperado: ~0.66 (4 Cs/Gs em 6 bases)

print(f"Resultado da função calcular_percentual_cg:{calcular_percentual_gc("ATCGCC"):.2f}")

# 8) contar_bases         — esperado: {"A": 2, "T": 1, "C": 1, "G": 1}
print(contar_bases("ATCGA"))

