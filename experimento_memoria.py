"""
Mede o pico de memória (KB) de cada algoritmo para cada cenário.
Pula automaticamente os algoritmos que já excederam timeout nos CSVs de tempo.
"""
import sys
import os
import csv
import threading
import tracemalloc

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

T = 10_000
N = 5
TIMEOUT = 60

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

GERADORES = {
    "crescente":   gerar_dados_crescente,
    "decrescente": gerar_dados_decrescente,
    "random":      gerar_dados_random,
}

CENARIOS = ["crescente", "decrescente", "random"]


def ler_timeouts_csv(caminho):
    """Retorna set de (rotulo, iteracao) onde o valor é negativo no CSV de tempo."""
    if not os.path.exists(caminho):
        return set()
    with open(caminho, newline="", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    timeouts = set()
    for i, row in enumerate(reader):
        for col, val in row.items():
            if int(val) < 0:
                timeouts.add((col, i))
    return timeouts


def medir_memoria(fn, dados, timeout=TIMEOUT):
    """Retorna pico de memória em KB, ou -1 se timeout/erro."""
    memoria_kb = [None]

    def _executar():
        try:
            tracemalloc.start()
            fn(dados.copy())
            _, pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memoria_kb[0] = pico / 1024
        except Exception:
            if tracemalloc.is_tracing():
                tracemalloc.stop()
            memoria_kb[0] = -1

    t = threading.Thread(target=_executar, daemon=True)
    t.start()
    t.join(timeout)

    if t.is_alive() or memoria_kb[0] is None:
        return -1
    return round(memoria_kb[0], 2)


sys.setrecursionlimit(100_000)
os.makedirs("docs", exist_ok=True)

for cenario in CENARIOS:
    print(f"\n=== Cenário: {cenario.upper()} ===")
    gerar = GERADORES[cenario]
    timeouts = ler_timeouts_csv(os.path.join("docs", f"resultado-{cenario}.csv"))

    resultados = []
    desativados = set()

    for i in range(1, N + 1):
        tamanho = i * T
        print(f"  Iteração {i:02d} — tamanho: {tamanho:,}")
        dados = gerar(tamanho)
        linha = []

        for rotulo, fn in ALGORITMOS:
            iter_idx = i - 1
            if rotulo in desativados or (rotulo, iter_idx) in timeouts:
                if rotulo not in desativados and (rotulo, iter_idx) in timeouts:
                    desativados.add(rotulo)
                linha.append(-2 if rotulo in desativados and (rotulo, iter_idx) not in timeouts else -1)
                print(f"    {rotulo:12s} — pulado (timeout no experimento de tempo)")
            else:
                mem = medir_memoria(fn, dados)
                if mem == -1:
                    desativados.add(rotulo)
                    print(f"    {rotulo:12s} — TIMEOUT → desativado")
                else:
                    print(f"    {rotulo:12s} — {mem:.2f} KB")
                linha.append(mem)

        resultados.append(linha)

    cabecalho = ",".join(r for r, _ in ALGORITMOS)
    linhas_csv = [cabecalho] + [",".join(str(v) for v in lin) for lin in resultados]
    nome = os.path.join("docs", f"resultado-{cenario}-memoria.csv")
    with open(nome, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_csv) + "\n")
    print(f"  Salvo em: {nome}")

print("\nDone.")
