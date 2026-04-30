# Algorithm Complexity Experiment - Recursion
PUCPR - Complexidade de Algoritmos - Projeto Colaborativo 1

## Descrição

Este projeto realiza uma análise experimental da **complexidade computacional** de diversos algoritmos de ordenação, comparando implementações:
- **Iterativas** vs **Recursivas**
- **Determinísticas** vs **Randomizadas**

O objetivo é validar empiricamente as complexidades teóricas (Big-O) desses algoritmos através da medição de tempo de execução em diferentes cenários de entrada.

## Propósito

Compreender na prática como a escolha entre recursão e iteração, assim como a estratégia de particionamento, afeta o desempenho real dos algoritmos de ordenação em cenários diferentes (dados crescentes, decrescentes e aleatórios).

## Algoritmos Implementados

| Acrônimo | Algoritmo | Tipo | Variação |
|----------|-----------|------|----------|
| **QS1** | Quick Sort | Recursivo | Tradicional (1º elemento) |
| **QS2** | Quick Sort | Recursivo | Randomizado (pivô aleatório) |
| **MS1** | Merge Sort | Iterativo | Bottom-up |
| **MS2** | Merge Sort | Recursivo | Tradicional |
| **MS3** | Merge Sort | Recursivo | Randomizado |
| **SS1** | Selection Sort | Recursivo | Tradicional |
| **SS2** | Selection Sort | Recursivo | Randomizado |
| **IS1** | Insertion Sort | Iterativo | Tradicional |
| **IS2** | Insertion Sort | Recursivo | Tradicional |
| **BASE_LINE** | Shell Sort | Iterativo | Baseline para comparação |

## Estrutura do Projeto

```
.
├── experimento.py              # Script principal de medição
├── gerador.py                  # Geração de dados de teste
├── grafico.py                  # Geração de gráficos e análise
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── algorithms/                 # Implementações dos algoritmos
│   ├── quick_sort_recursivo.py
│   ├── quick_sort_random.py
│   ├── merge_sort_interativo.py
│   ├── merge_sort_recursivo.py
│   ├── merge_sort_recursivo_random.py
│   ├── select_sort_recursivo.py
│   ├── select_sort_recursivo_random.py
│   ├── Insertion_sort_interativo.py
│   ├── insertion_sort_recursivo.py
│   └── sellSort_base_line.py
└── docs/                       # Resultados e gráficos
    ├── resultado-crescente.csv
    ├── resultado-decrescente.csv
    ├── resultado-random.csv
    └── graficos/
        ├── QS1.png
        ├── MS1.png
        ├── ... (um gráfico por algoritmo)
        └── resumo.png
```

## Requisitos

- **Python 3.8+**
- Dependências: `numpy`, `matplotlib`

Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Executar

### 1. Executar o Experimento
Coleta dados de tempo de execução para todos os algoritmos:
```bash
python experimento.py
```

**Configuração do experimento** (em `experimento.py`):
- `T = 250` — tamanho base do problema
- `N = 20` — número de iterações
- `CENARIO = "crescente"` — mudar para `"decrescente"` ou `"random"`

O script gera um arquivo CSV em `docs/resultado-{cenario}.csv` com os tempos em milissegundos.

### 2. Gerar Gráficos
Cria visualizações com regressão polinomial e análise de R²:
```bash
python grafico.py
```

**Configuração dos gráficos** (em `grafico.py`):
- `GRAU = 2` — grau do polinômio de regressão (2 = quadrático)
- `SALVAR = True` — salva PNGs em `docs/graficos/`

Gera:
- Um gráfico individual por algoritmo (com todas as cenários)
- Um painel resumo com todos os algoritmos em grid

## Saídas Esperadas

### Arquivos CSV
Cada linha contém os tempos (em ms) dos 10 algoritmos para um tamanho de entrada específico:
```
QS1,QS2,MS1,MS2,MS3,SS1,SS2,BASE_LINE,IS1,IS2
45,42,38,40,41,1250,1248,35,890,920
```

### Gráficos
- **Individual**: Um gráfico por algoritmo com os 3 cenários (crescente, decrescente, random)
- **Equação de regressão**: $f(x) = ax^2 + bx + c$ 
- **R²**: Coeficiente de determinação (qualidade do ajuste polinomial)
- **Resumo**: Painel 5×2 com todos os algoritmos para comparação rápida

## Análises Esperadas

### Complexidade Observada
- **Merge Sort**: $O(n \log n)$ — desempenho consistente em todos os cenários
- **Quick Sort**: 
  - Tradicional: $O(n^2)$ em piores casos (dados já ordenados)
  - Randomizado: $O(n \log n)$ em média, mais robusto
- **Selection Sort**: $O(n^2)$ independente da entrada
- **Insertion Sort**: $O(n)$ em melhores casos, $O(n^2)$ em piores
- **Shell Sort**: Entre $O(n \log n)$ e $O(n^2)$ dependendo do gap sequence

### Impacto da Recursão
Algoritmos recursivos podem ser **mais lentos** que iterativos equivalentes devido ao overhead de chamadas de função e stack, especialmente em listas grandes.

## Configuração do Experimento

Para investigar diferentes cenários, edite `experimento.py`:

```python
T = 250     # Aumentar para testar com lista maiores
N = 20      # Aumentar para mais iterações (dados mais suavizados)
CENARIO = "crescente"   # Mudar para "decrescente" ou "random"
```

Limite de recursão:
```python
sys.setrecursionlimit(100_000)  # Aumentar se necessário para listas muito grandes
```

## Interpretação dos Gráficos

Cada gráfico mostra:
1. **Pontos dispersos**: dados reais coletados
2. **Linha contínua**: regressão polinomial (curva ajustada)
3. **Equação**: $f(x) = $ equação do polinômio
4. **R²**: qualidade do ajuste (próximo a 1 = excelente)

Uma função $O(n^2)$ será representada por um polinômio de grau 2, enquanto $O(n \log n)$ se aproximará mais de um polinômio de grau 2 mas com coeficientes menores.

## 📝 Autores
- Angelo Netho
- Angelo Piovezan
- Hugo Fagundes
- Renato Gouveia
