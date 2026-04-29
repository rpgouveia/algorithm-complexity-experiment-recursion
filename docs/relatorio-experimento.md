# Relatório de Complexidade de Algoritmos de Ordenação

Este relatório apresenta a análise dos resultados obtidos no experimento de tempo de execução de vários algoritmos de ordenação implementados no projeto.

## Configuração do Experimento
- **Script principal:** `experimento.py`
- **Tamanho base (T):** 250 elementos
- **Iterações (N):** 20
- **Tamanho máximo da estrutura:** 5000 elementos
- **Cenário de Dados:** Foi utilizada a função `gerar_dados_decrescente()`, submetendo os algoritmos ao pior cenário clássico de uma lista já ordenada ao contrário.

## Resultados Obtidos (em milisegundos)

| Tamanho | QS1 (Quick) | QS2 (Quick Rand.) | MS1 (Merge Iter.) | MS2 (Merge Rec.) | MS3 (Merge Rand.) | SS1 (Select Rec.) | SS2 (Select Rand.) | BASE_LINE (Shell) |
|---------|-------------|-------------------|-------------------|------------------|-------------------|-------------------|--------------------|-------------------|
| 250 | 3 | 0 | 1 | 0 | 0 | 5 | 18 | 57 |
| 500 | 17 | 1 | 1 | 1 | 2 | 22 | 72 | 90 |
| 750 | 27 | 2 | 1 | 1 | 2 | 46 | 170 | 113 |
| 1000 | 44 | 1 | 2 | 1 | 2 | 66 | 265 | 196 |
| 1250 | 70 | 2 | 2 | 2 | 3 | 106 | 452 | 177 |
| 1500 | 121 | 2 | 3 | 2 | 4 | 184 | 737 | 291 |
| 1750 | 175 | 3 | 3 | 3 | 6 | 255 | 1012 | 248 |
| 2000 | 226 | 5 | 6 | 3 | 7 | 338 | 1411 | 340 |
| 2250 | 258 | 4 | 5 | 4 | 5 | 373 | 1549 | 342 |
| 2500 | 324 | 4 | 6 | 4 | 6 | 545 | 2192 | 364 |
| 2750 | 390 | 5 | 6 | 5 | 7 | 680 | 2616 | 511 |
| 3000 | 470 | 6 | 6 | 5 | 8 | 624 | 3020 | 483 |
| 3250 | 662 | 7 | 7 | 6 | 9 | 901 | 4318 | 828 |
| 3500 | 534 | 6 | 6 | 5 | 7 | 880 | 4525 | 652 |
| 3750 | 614 | 6 | 6 | 5 | 9 | 1202 | 5177 | 674 |
| 4000 | 819 | 6 | 8 | 6 | 9 | 1286 | 6059 | 756 |
| 4250 | 822 | 7 | 8 | 7 | 10 | 1376 | 7172 | 917 |
| 4500 | 880 | 8 | 9 | 8 | 12 | 1671 | 7406 | 912 |
| 4750 | 987 | 13 | 11 | 9 | 14 | 2007 | 8360 | 818 |
| 5000 | 1118 | 10 | 12 | 8 | 14 | 2187 | 9293 | 748 |

---

## Análise de Desempenho

### 1. Merge Sort (MS1, MS2, MS3) - Campeões em Estabilidade
Os algoritmos baseados em Merge Sort demonstraram tempos baixíssimos do início ao fim (entre 8 e 14 ms constantes no final do teste).

**Explicação Teórica:** 
O Merge Sort tem complexidade assintótica $O(n \log n)$ invariável. Não importa se a lista inicial está caótica ou invertida; o escopo comportamental de "dividir para conquistar" mantém sua excelente alta performance no melhor e pior caso.

### 2. O Extremo Oposto: A Queda do Quick Sort (QS1 vs QS2)
Houve uma discrepância gigantesca em relação ao Quick Sort clássico versus as versões balanceadas randomizadas.

- **QS1 (Tradicional):** Iniciou relativamente rápido e sofreu decaimento exponencial extremo, sendo o último com 1118 ms. **Motivo?** A matriz totalmente decrescente fez o algoritmo se deparar com sua pior complexidade teórica possível de $O(n^2)$.
- **QS2 (Randomizado):** Finalizou de forma assustadoramente brilhante em longínquos **10 ms**.
**Motivo?** Por escolher um número aleatoriamente no papel de pivô, a complexidade consegue esquivar da anomalia do pior caso garantindo um resultado sempre equilibradamente particionado, voltando a complexidade para $O(n \log n)$.

### 3. Selection Sort (SS1 e SS2) - Punição Natural
Constata-se baixa adequação geral desse algoritmo a amplos volumes de dados:
- **SS1 (Recursivo):** Custosos **2187 ms**.
- **SS2 (Randomizado):** Tempo insustentável de **9293 ms**.

**Explicação Teórica:** 
A complexidade estrutural de Selection Sort baseia-se num tempo imutável de $O(n^2)$. A introdução das chamadas aleatórias extras no SS2 agravou radicalmente um método que, por padrão, já é exaustivo.

### 4. Shell Sort (BASE_LINE)
Embasamento do experimento, o Shell Sort marcou **748 ms**.  Ficou provado que, perante situações de pior caso, o algoritmo Shell resistiu consideravelmente melhor a listas de dados invertidas em detrimento direto ao Selection e Quick clássico; muito embora seu desempenho nem de longe acompanhe as classes $O(n \log n)$ em tempo linear.

## Conclusões Gerais
O experimento empírico prova de forma precisa e cristalina que a qualidade individual (ou fator matemático randômico) empregada sobre um algoritmo define de maneira letal sua adequação nos piores cenários de engenharia de software e análise de dados. Recomendam-se amplamente instâncias baseadas em lógica *Merge* ou variantes randomizadas particionadas para listas extensas desconhecidas.
