# O Projeto: um panorama da família Flaviviridae
#
# Leia o enunciado completo no README (seção "O Projeto")
#
# A ideia é construir UMA tabela (pandas) descrevendo os vírus e, a partir dela,
# tirar duas conclusões:
#   - o conteúdo GC é aleatório? (Parte 2)
#   - quão grande é a proteína de cada vírus? (Parte 3)
#
# Vá preenchendo as partes abaixo, uma de cada vez.
# Obs: Se preferir fazer esse processo num jupyter notebook, sem problemas!! Fica a critério do grupo

import pandas as pd

pd.set_option('display.max_columns', None)   # mostra todas as colunas
pd.set_option('display.width', None)         # não quebra linha por largura do terminal
pd.set_option('display.max_colwidth', 30)

from bio.ler_fasta import ler_fasta
from bio.sequencia import (
    traduzir,
    calcular_percentual_gc,
    encontrar_inicio,
)


# ------------------------------------------------------------------
# Parte 1 — Monte a tabela
# ------------------------------------------------------------------
organismos = ler_fasta("arquivos/Flaviviridae-genomes.fasta")
df = pd.DataFrame(organismos)
df["tamanho"] = df["sequencia"].apply(len)

print("Primeiras linhas da tabela:")
print(df.head())


# ------------------------------------------------------------------
# Parte 2 — O conteúdo GC é aleatório?
# ------------------------------------------------------------------
# 1) crie a coluna "gc" com df["sequencia"].apply(calcular_percentual_gc)
# 2) mostre os 10 maiores e os 10 menores GC (com o nome!) -> usar função sort_values do pandas
# 3) escreva sua conclusão sobre o padrão que observou
df["gc"] = df["sequencia"].apply(calcular_percentual_gc)

df_maior_gc = df.sort_values("gc", ascending=False)
df_menor_gc = df.sort_values("gc", ascending=True)

print("\n10 vírus com maior GC:")
print(df_maior_gc[["nome", "gc"]].head(10))

print("\n10 vírus com menor GC:")
print(df_menor_gc[["nome", "gc"]].head(10))

print("\nConclusão sobre GC:")
print(
    "Os extremos de GC não parecem aleatórios: vírus com nomes parecidos aparecem "
    "agrupados entre os maiores ou menores valores. Isso sugere que vírus mais "
    "relacionados também se parecem na composição de bases do genoma."
)


# ------------------------------------------------------------------
# Parte 3 — Encontre a proteína (a poliproteína viral)
# ------------------------------------------------------------------
# 1) coluna "proteina": traduzir(encontrar_inicio(seq), parar=True)
# 2) coluna "tamanho_proteina": len da proteína
# 3) coluna "cobertura": (tamanho_proteina * 3) / tamanho
# 4) escreva sua conclusão (qual a cobertura típica? faz sentido ser 1 poliproteína?)
df["sequencia_inicio"] = df["sequencia"].apply(encontrar_inicio)
df["proteina"] = df["sequencia_inicio"].apply(lambda sequencia: traduzir(sequencia, parar=True))
df["tamanho_proteina"] = df["proteina"].apply(len)
df["cobertura"] = (df["tamanho_proteina"] * 3) / df["tamanho"]

print("\nTamanhos de proteína e cobertura:")
print(df[["nome", "tamanho", "tamanho_proteina", "cobertura"]].head(10))

cobertura_tipica = df["cobertura"].median()

print("\nConclusão sobre a proteína:")
print(f"A cobertura típica é {cobertura_tipica:.2f}.")
print(
    "Para a maioria dos vírus, a proteína ocupa uma parte grande do genoma, "
    "o que combina com a ideia de uma única poliproteína viral. Alguns casos "
    "ficam com cobertura baixa porque o primeiro ATG encontrado pode não ser "
    "o início correto do gene."
)


# ------------------------------------------------------------------
# Parte 4 — Salve o resultado
# ------------------------------------------------------------------
# 1) filtre os vírus com gc > 0.5 (quantos são?)
# 2) df.to_csv("resultado.csv", index=False)
df_gc_alto = df[df["gc"] > 0.5]

print("\nVírus com GC acima de 50%:")
print(len(df_gc_alto))

df.to_csv("resultado.csv", index=False)
print("\nTabela salva em resultado.csv")
