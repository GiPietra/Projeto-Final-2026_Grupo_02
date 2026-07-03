# Projeto - Escrevendo nossa própria "BioPython"

Para treinar o que aprendemos durante o curso, vamos criar algumas funções inspiradas na
biblioteca BioPython. E vamos usá-las para resolver alguns problemas de Bioinformática.

Vai ser algo simplificado, apenas com o intuito de treinarmos as ferramentas que vimos em
sala de aula: strings, listas, dicionários, funções e, no final, **pandas**.

--------------------------

## Como rodar os scripts

Rode direto da raiz do projeto:

```
python exercicios_funcoes.py
python projeto.py
```

--------------------------

## Preparando o ambiente

O último problema usa a biblioteca **pandas**. Para instalá-la, rode no terminal:

```
pip install -r requirements.txt
```

--------------------------

## Como os dados são representados

Nada de classes por aqui! Vamos usar só o que já conhecemos:

- Uma **sequência** de DNA é uma **string**. Ex: `"ATCG"`.
- Um **organismo** (uma entrada do arquivo FASTA) é um **dicionário** com três chaves:
  `{"id": "NC_074786.1", "nome": "Guereza hepacivirus...", "sequencia": "CACTCC..."}`.
- Um **arquivo FASTA inteiro** vira uma **lista de dicionários** (um dicionário por organismo).

Esse formato é bem prático: dá para percorrer com um `for`, e no exercício de pandas ele
vira uma tabela com uma linha por organismo.

--------------------------

## De onde vêm os dados: o arquivo `arquivos/Flaviviridae-genomes.fasta`

### O que é o NCBI

O **NCBI** (National Center for Biotechnology Information) é um instituto público
americano que mantém as maiores bases de dados biológicos do mundo — sequências de DNA,
RNA, proteínas, genomas inteiros, artigos científicos, etc. Praticamente todo pesquisador
de biologia molecular do planeta usa (ou já usou) dados de lá.

Dentro do NCBI existe o **RefSeq**, uma coleção "curada" de genomas de referência: para
cada organismo (ou vírus), o RefSeq guarda uma sequência representativa, revisada e bem
anotada, identificada por um código no formato `NC_XXXXXX.X` (repare que é exatamente o
prefixo dos IDs no nosso FASTA, tipo `NC_001477.1`).

O arquivo `arquivos/Flaviviridae-genomes.fasta` foi baixado direto do RefSeq/NCBI: ele
reúne os genomas de referência de **todos os vírus classificados na família
Flaviviridae** — 159 vírus ao todo. Cada entrada do FASTA é um vírus diferente, com seu
próprio genoma completo (ou quase completo — alguns são "partial genome", genoma
parcial).

### Por que a família Flaviviridae importa

Flaviviridae é uma família de vírus de RNA de fita simples, muitos deles transmitidos por
mosquitos ou carrapatos, e ela inclui alguns dos patógenos humanos mais relevantes da
história recente:

- **Dengue virus** (4 sorotipos diferentes no arquivo: Dengue 1 a 4)
- **Zika virus**
- **Yellow fever virus** (febre amarela)
- **West Nile virus** (febre do Nilo Ocidental)
- **Hepatitis C virus** (hepatite C, várias genótipos no arquivo)

Além desses, o arquivo tem dezenas de vírus menos conhecidos do público, mas igualmente
estudados: pestivírus de gado e porcos (como o *Bovine viral diarrhea virus*, que causa
prejuízos enormes na pecuária), vírus encontrados em morcegos, roedores, pangolins,
golfinhos e até em insetos — o que ajuda cientistas a entender de onde vírus novos podem
"pular" para humanos (spillover).

Ou seja: é uma família com nomes de peso em saúde pública, mas também um bom exemplo de
como a mesma "receita" genômica (a poliproteína única, que vamos explorar na Parte 3) se
repete em vírus que infectam hospedeiros completamente diferentes.

### O que vamos analisar

Vamos usar as suas funções para transformar esse arquivo de texto (só letras A, C, G, T)
numa tabela e responder duas perguntas biológicas de verdade:

1. Vírus parecidos (mesmo gênero, mesmo tipo de hospedeiro) têm uma composição química de
   DNA parecida? É isso que a análise de **conteúdo GC** vai revelar (Parte 2).
2. Será que todos esses vírus organizam seu genoma do mesmo jeito, com uma única
   **poliproteína** cobrindo quase o genoma inteiro? (Parte 3)

As respostas estão descritas em detalhe na seção "Usando as suas funções", mais abaixo.

--------------------------

## Já está pronto para você (código de apoio)

### Função `ler_fasta(caminho_do_arquivo)`  —  em `bio/ler_fasta.py`

Inspirada na `SeqIO.parse`. **Você não precisa escrever esta função**, ela já está pronta.
Ela lê um arquivo FASTA e devolve a **lista de dicionários** descrita acima.

```python
from bio.ler_fasta import ler_fasta

organismos = ler_fasta("arquivos/Flaviviridae-genomes.fasta")
print(organismos[0]["nome"])        # nome do primeiro organismo
print(organismos[0]["sequencia"])   # sequência (string) do primeiro organismo
```

### Constantes  —  em `bio/constantes.py`

- `DNA_PARA_AMINOACIDO`: dicionário que traduz cada códon (trinca) no seu aminoácido.
- `DNA_STOP_CODONS`: lista com os códons de parada (stop codons).

--------------------------

## Para ser criado por você

Todas estas funções ficam em `bio/sequencia.py` (já com o esqueleto e dicas). Cada uma
recebe a sequência como uma **string** e devolve um resultado.

- `complementar(sequencia)` — inspirado no `Seq().complement()`
  - Retorna a string da sequência complementar (A<->T, C<->G).
  - Ex: `complementar("ATCG")` -> `"TAGC"`

- `complementar_reversa(sequencia)` — inspirado no `Seq().reverse_complement()`
  - Retorna a string da sequência complementar reversa.
  - Ex: `complementar_reversa("ATCG")` -> `"CGAT"`

- `transcrever(sequencia)` — inspirado no `Seq().transcribe()`
  - Retorna a string resultante da transcrição (DNA -> RNA; o T vira U).
  - Ex: `transcrever("ATCG")` -> `"AUCG"`

- `traduzir(sequencia, parar=False)` — inspirado no `Seq().translate()`
  - Retorna uma string com a tradução da sequência para uma proteína.
  - Ex: `traduzir("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")` -> `"MAIVMGR*KGAR*"`
  - Leia a sequência de 3 em 3 (cada trinca é um códon) e use o dicionário
    `DNA_PARA_AMINOACIDO`. Stop codons viram `*`; trincas fora do dicionário (base
    indefinida) viram `X`.
  - Se `parar=True`, a tradução para no primeiro stop codon. Se `parar=False`, continua
    até o fim marcando os stops como `*`.

- `calcular_percentual(sequencia, bases)` — (inventada por nós)
  - Recebe uma lista de bases e retorna o percentual delas na sequência.
  - Ex: `calcular_percentual("ATCGAAA", ["A"])` -> `0.5`
  - Ex: `calcular_percentual("ATCGCC", ["C", "G"])` -> `~0.66`

- `contar_bases(sequencia)` — (inventada por nós)
  - Retorna um dicionário com a contagem de cada base.
  - Ex: `contar_bases("ATCGA")` -> `{"A": 2, "T": 1, "C": 1, "G": 1}`

- `encontrar_inicio(sequencia)` — (inventada por nós)
  - Retorna a sequência a partir do primeiro **start codon** (`ATG`), que é onde a tradução
    de um gene começa. Se não houver `ATG`, retorna uma string vazia `""`.
  - Ex: `encontrar_inicio("CCATGGGGTAA")` -> `"ATGGGGTAA"`
  - Usamos ela junto com `traduzir` para achar a proteína: `traduzir(encontrar_inicio(seq), parar=True)`.

----------------------

# Usando as suas funções

Depois de criar as funções em `bio/sequencia.py`, você tem **duas entregas**:

1. **`exercicios_funcoes.py`** — testar cada função isoladamente. Mostra que você domina o
   básico. (Veja a primeira seção abaixo.)
2. **`projeto.py`** — a investigação completa dos vírus da família Flaviviridae, montando uma
   tabela com pandas e tirando conclusões. É aqui que você mostra que sabe *aplicar* as
   funções num problema real. (Veja "O Projeto", mais abaixo.)

=================================================================

# Entrega 1 — Exercícios das funções (`exercicios_funcoes.py`)

Confira que cada função que você criou funciona numa sequência pequena. Para cada uma,
escreva um `print` e veja se o resultado bate com o esperado:

- `complementar("ATCG")` -> `"TAGC"`
- `complementar_reversa("ATCG")` -> `"CGAT"`
- `transcrever("ATCG")` -> `"AUCG"`
- `encontrar_inicio("CCCATGGGGTAA")` -> `"ATGGGGTAA"` (começa no 1º `ATG`)
- `traduzir("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG")` -> `"MAIVMGR*KGAR*"`
- `traduzir(..., parar=True)` -> deve parar no primeiro stop codon
- `calcular_percentual("ATCGAAAA", ["A"])` -> `0.5`
- `contar_bases("ATCGA")` -> `{"A": 2, "T": 1, "C": 1, "G": 1}`

O arquivo `exercicios_funcoes.py` já vem com os blocos prontos para você preencher.

=================================================================

# Entrega 2 — O Projeto: um panorama da família Flaviviridae (`projeto.py`)

O arquivo `arquivos/Flaviviridae-genomes.fasta` reúne os genomas de referência de **toda a
família viral _Flaviviridae_** — mais de 150 vírus diferentes, incluindo velhos conhecidos
como **Dengue, Zika, Febre Amarela e Hepatite C**. São vírus aparentados, mas de gêneros
distintos (Orthoflavivirus, Hepacivirus, Pestivirus, Pegivirus...).

Nossa meta é montar uma **tabela** (com pandas) descrevendo esses vírus e, a partir dela,
responder a duas perguntas:

1. O **conteúdo GC** dos genomas é distribuído ao acaso, ou vírus parecidos se parecem também nisso?
2. Esses vírus têm um genoma organizado de forma parecida? Quão grande é a **proteína** que cada um produz?

Vamos construir isso por partes. Cada função que você escreveu vai virar uma peça da análise.

---------------------------

## Parte 1 — Montando a tabela

**Objetivo:** transformar os dados do FASTA numa tabela do pandas, onde cada linha é um vírus.

1. Leia o arquivo com `ler_fasta` (ele devolve uma lista de dicionários).
2. Monte o DataFrame: `df = pd.DataFrame(organismos)`. Você deve ter as colunas
   `id`, `nome` e `sequencia`.
3. Crie a coluna `tamanho` com o número de bases de cada genoma.

Dicas:
```python
import pandas as pd
from bio.ler_fasta import ler_fasta

organismos = ler_fasta("arquivos/Flaviviridae-genomes.fasta")
df = pd.DataFrame(organismos)
df["tamanho"] = df["sequencia"].apply(len)
```

---------------------------

## Parte 2 — O conteúdo GC é aleatório?

**Objetivo:** usar a coluna de GC para investigar se vírus parecidos têm GC parecido.

O **conteúdo GC** é o percentual de bases C + G no genoma. Ele varia de vírus para vírus.
Vamos ver se essa variação diz alguma coisa.

1. Crie a coluna `gc` usando a sua função `calcular_percentual`.
2. **Ordene** a tabela por `gc` e mostre, **com o nome**, os 10 vírus de **maior** GC e os
   10 de **menor** GC.
3. **Conclusão (escreva num `print` ou comentário):** olhe os nomes dos dois extremos.
   Os vírus de GC mais alto parecem ser do mesmo tipo entre si? E os de GC mais baixo?
   Repare nas palavras que se repetem nos nomes. O GC parece aleatório ou não?

Dicas:
```python
df["gc"] = df["sequencia"].apply(lambda s: calcular_percentual(s, ["G", "C"]))
df.sort_values("gc", ascending=False)[["nome", "gc"]].head(10)   # maior GC
df.sort_values("gc")[["nome", "gc"]].head(10)                     # menor GC
```

---------------------------

## Parte 3 — Encontrando a proteína (a poliproteína viral)

**Objetivo:** usar `encontrar_inicio` + `traduzir` para descobrir o tamanho da proteína de
cada vírus, e ver o que isso revela sobre a organização do genoma.

Um detalhe importante de biologia: nos Flaviviridae, o genoma inteiro é traduzido como
**uma única proteína gigante** (chamada *poliproteína*), que depois a célula corta em
pedaços menores. Repare que os nomes no FASTA dizem "**polyprotein**"!

Mas atenção: a tradução do gene **não começa na primeira base** do genoma — há um trecho
inicial que não é traduzido. Por isso precisamos primeiro achar o **start codon** (`ATG`)
com a sua função `encontrar_inicio`, e só então traduzir.

1. Crie a coluna `proteina`: para cada sequência, ache o início com `encontrar_inicio` e
   traduza **parando no primeiro stop codon** (`parar=True`).
2. Crie a coluna `tamanho_proteina` com o número de aminoácidos dessa proteína.
3. Crie a coluna `cobertura`: quanto do genoma essa proteína ocupa. Como cada aminoácido
   vem de 3 bases, isso é `(tamanho_proteina * 3) / tamanho`.
4. **Conclusão (escreva num `print` ou comentário):** qual é a cobertura *típica* (use
   `df["cobertura"].median()`)? Para a maioria dos vírus, a proteína cobre uma parte grande
   do genoma? Isso combina com a ideia de que esses vírus têm **uma** poliproteína só?
   (Você também vai notar alguns casos com cobertura baixa — nesses, o primeiro `ATG` que
   achamos não era o começo certo do gene. Não tem problema, comente que isso acontece.)

Dicas:
```python
df["proteina"] = df["sequencia"].apply(lambda s: traduzir(encontrar_inicio(s), parar=True))
df["tamanho_proteina"] = df["proteina"].apply(len)
df["cobertura"] = (df["tamanho_proteina"] * 3) / df["tamanho"]
```

---------------------------

## Parte 4 — Salvando o resultado

**Objetivo:** guardar a sua tabela final para consulta.

1. **Filtre** a tabela para ver só os vírus com GC acima de 50% (`df["gc"] > 0.5`) —
   quantos são?
2. **Salve** a tabela completa num arquivo `.csv`.

Dica:
```python
df.to_csv("resultado.csv", index=False)
```

Pronto! Você partiu de um arquivo de texto com 150+ genomas e chegou a uma tabela que
revela padrões reais da biologia desses vírus. É exatamente assim que se começa uma análise
de bioinformática.

-----------------------

## Avaliação

Diferente das nossas tarefas de casa, não terá avaliação automática. Eu vou ler e avaliar
e dar uma nota com cuidado.

Então mesmo se não funcionar 100%, eu vou conseguir dar nota de acordo com a solução.
</content>
