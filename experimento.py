import sys
import os
import threading
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
T = 10_000              # tamanho base: 10.000 elementos
N = 5                   # iterações → 10k, 20k, 30k, 40k, 50k
CENARIO = "random"   # "crescente" | "decrescente" | "random"
TIMEOUT = 60            # segundos

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
def medir_com_timeout(fn, dados, timeout=TIMEOUT):
    """
    Executa fn(dados) em uma thread separada.
    Retorna o tempo em ms, ou -1 se ultrapassar `timeout` segundos.
    O valor -1 indica que o algoritmo foi descartado por exceder 1 minuto,
    conforme requisito do enunciado.
    """
    resultado = [None]

    def _executar():
        try:
            a = agora()
            fn(dados.copy())
            resultado[0] = dif_time(agora(), a)
        except Exception:
            resultado[0] = -1

    t = threading.Thread(target=_executar, daemon=True)
    t.start()
    t.join(timeout)

    if t.is_alive() or resultado[0] is None:
        return -1   # timeout atingido
    return resultado[0]


def execucao(dados, desativados):
    """
    Executa todos os algoritmos sobre uma cópia dos dados.
    Algoritmos em `desativados` são pulados (já excederam 1 min antes).
    Retorna lista de tempos; -1 = timeout, -2 = pulado.
    """
    tempos = []
    for rotulo, fn in ALGORITMOS:
        if rotulo in desativados:
            tempos.append(-2)
            print(f"    {rotulo:12s} — pulado (timeout anterior)")
        else:
            t = medir_com_timeout(fn, dados)
            if t == -1:
                desativados.add(rotulo)
                print(f"    {rotulo:12s} — TIMEOUT (> {TIMEOUT}s) → desativado")
            else:
                print(f"    {rotulo:12s} — {t} ms")
            tempos.append(t)
    return tempos


def teste():
    """Smoke test rápido para verificar que todos os algoritmos ordenam corretamente."""
    referencia = [-1, 2, 21, 24, 30, 35, 48, 58, 59, 81, 97]
    entrada = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]

    for rotulo, fn in ALGORITMOS:
        resultado = fn(entrada.copy())
        ok = "✓" if resultado == referencia else "✗"
        print(f"  {ok} {rotulo}: {resultado}")


# Execução principal
sys.setrecursionlimit(100_000)
print(f"Limite de recursão : {sys.getrecursionlimit()}")
print(f"Cenário            : {CENARIO}")
print(f"Tamanhos           : {[i * T for i in range(1, N + 1)]}")
print(f"Timeout            : {TIMEOUT}s\n")

gerar = GERADORES[CENARIO]
resultados = []
desativados = set()   # algoritmos que já excederam 1 minuto

for i in range(1, N + 1):
    tamanho = i * T
    print(f"Iteração {i:02d} — tamanho: {tamanho:,}")
    X = gerar(tamanho)
    resultados.append(execucao(X, desativados))
    print()


# Impressão e salvamento CSV
cabecalho = ",".join(rotulo for rotulo, _ in ALGORITMOS)
linhas_csv = [cabecalho] + [",".join(str(t) for t in linha) for linha in resultados]
print("\n" + "\n".join(linhas_csv))

os.makedirs("docs", exist_ok=True)
nome_arquivo = os.path.join("docs", f"resultado-{CENARIO}.csv")
with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_csv) + "\n")

print(f"\nResultados salvos em: {nome_arquivo}")

if desativados:
    print(f"\nAlgoritmos desativados por timeout: {', '.join(sorted(desativados))}")
    print("Seus valores no CSV estão marcados como -1 (timeout) ou -2 (pulado).")