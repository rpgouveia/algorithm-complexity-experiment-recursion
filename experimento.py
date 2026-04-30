import sys
import os
from algorithms.quick_sort_recursivo import quick_sort_recursivo_wapper
from algorithms.quick_sort_random import quick_sort_recursivo_random_wapper
from algorithms.merge_sort_interativo import Merge_Sort_interativo_wapper
from algorithms.merge_sort_recursivo import merge_sort__recursivo_wapper
from algorithms.merge_sort_recursivo_random import merge_sort_recursivo_random_wapper
from algorithms.select_sort_recursivo import select_sort_recursivo_wapper
from algorithms.select_sort_recursivo_random import select_sort_recursivo_random_wapper
from algorithms.sellSort_base_line import shellSort_Wapper
from algorithms.Insertion_sort_interativo import insertion_sort_interativo
from algorithms.insertion_sort_recursivo import IS_recursivo
from gerador import gerar_dados_crescente, gerar_dados_random, gerar_dados_decrescente
from gerador import agora, dif_time


# Configurações do experimento
T = 250     # tamanho base do problema
N = 20      # número de iterações
CENARIO = "crescente"   # "crescente" | "decrescente" | "random"

GERADORES = {
    "crescente":   gerar_dados_crescente,
    "decrescente": gerar_dados_decrescente,
    "random":      gerar_dados_random,
}

# Tabela de algoritmos: (rótulo CSV, função wrapper)
ALGORITMOS = [
    ("QS1",       quick_sort_recursivo_wapper),
    ("QS2",       quick_sort_recursivo_random_wapper),
    ("MS1",       Merge_Sort_interativo_wapper),
    ("MS2",       merge_sort__recursivo_wapper),
    ("MS3",       merge_sort_recursivo_random_wapper),
    ("SS1",       select_sort_recursivo_wapper),
    ("SS2",       select_sort_recursivo_random_wapper),
    ("BASE_LINE", shellSort_Wapper),
    ("IS1",       insertion_sort_interativo),
    ("IS2",       IS_recursivo),
]


# Funções auxiliares
def medir(fn, dados):
    """Executa fn(dados) e retorna o tempo gasto em milissegundos."""
    a = agora()
    fn(dados)
    return dif_time(agora(), a)


def execucao(dados):
    """
    Executa todos os algoritmos sobre uma cópia dos dados de entrada e
    retorna a lista de tempos de execução em milissegundos.
    """
    return [medir(fn, dados.copy()) for _, fn in ALGORITMOS]


def teste():
    """Smoke test rápido para verificar que todos os algoritmos ordenam corretamente."""
    referencia = [-1, 2, 21, 24, 30, 35, 48, 58, 59, 81, 97]
    entrada = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]

    for rotulo, fn in ALGORITMOS:
        resultado = fn(entrada.copy())
        ok = "✓" if resultado == referencia else "✗"
        print(f"  {ok} {rotulo}: {resultado}")


# Execução principal
# Aumenta o limite de recursão para os algoritmos recursivos profundos
sys.setrecursionlimit(100_000)
print(f"Limite de recursão: {sys.getrecursionlimit()}")

gerar = GERADORES[CENARIO]
resultados = []

for i in range(1, N + 1):
    tamanho = i * T
    print(f"Iteração {i:02d} — tamanho: {tamanho}")
    X = gerar(tamanho)
    resultados.append(execucao(X))

# Imprime e salva CSV
cabecalho = ",".join(rotulo for rotulo, _ in ALGORITMOS)
linhas_csv = [cabecalho] + [",".join(str(t) for t in linha) for linha in resultados]
print("\n".join(linhas_csv))

os.makedirs("docs", exist_ok=True)
nome_arquivo = os.path.join("docs", f"resultado-{CENARIO}.csv")
with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_csv) + "\n")

print(f"\nResultados salvos em: {nome_arquivo}")