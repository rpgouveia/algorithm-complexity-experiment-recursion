import sys
import os
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
    Retorna (tempo_ms, pico_kb), ou (-1, -1) se ultrapassar `timeout` segundos.
    """
    resultado = [None]
    memoria_kb = [None]

    def _executar():
        try:
            tracemalloc.start()
            a = agora()
            fn(dados.copy())
            tempo = dif_time(agora(), a)
            _, pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            resultado[0] = tempo
            memoria_kb[0] = pico / 1024
        except Exception:
            if tracemalloc.is_tracing():
                tracemalloc.stop()
            resultado[0] = -1
            memoria_kb[0] = -1

    t = threading.Thread(target=_executar, daemon=True)
    t.start()
    t.join(timeout)

    if t.is_alive() or resultado[0] is None:
        return -1, -1   # timeout atingido
    return resultado[0], memoria_kb[0]


def execucao(dados, desativados):
    """
    Executa todos os algoritmos sobre uma cópia dos dados.
    Algoritmos em `desativados` são pulados (já excederam 1 min antes).
    Retorna (lista_tempos, lista_memorias_kb); -1 = timeout, -2 = pulado.
    """
    tempos = []
    memorias = []
    for rotulo, fn in ALGORITMOS:
        if rotulo in desativados:
            tempos.append(-2)
            memorias.append(-2)
            print(f"    {rotulo:12s} — pulado (timeout anterior)")
        else:
            t, mem = medir_com_timeout(fn, dados)
            if t == -1:
                desativados.add(rotulo)
                print(f"    {rotulo:12s} — TIMEOUT (> {TIMEOUT}s) → desativado")
            else:
                print(f"    {rotulo:12s} — {t} ms | {mem:.1f} KB")
            tempos.append(t)
            memorias.append(round(mem, 2) if mem >= 0 else mem)
    return tempos, memorias


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
resultados_tempo = []
resultados_memoria = []
desativados = set()   # algoritmos que já excederam 1 minuto

for i in range(1, N + 1):
    tamanho = i * T
    print(f"Iteração {i:02d} — tamanho: {tamanho:,}")
    X = gerar(tamanho)
    tempos, memorias = execucao(X, desativados)
    resultados_tempo.append(tempos)
    resultados_memoria.append(memorias)
    print()


# Impressão e salvamento CSV
cabecalho = ",".join(rotulo for rotulo, _ in ALGORITMOS)
os.makedirs("docs", exist_ok=True)

linhas_tempo = [cabecalho] + [",".join(str(t) for t in linha) for linha in resultados_tempo]
print("\n" + "\n".join(linhas_tempo))
nome_tempo = os.path.join("docs", f"resultado-{CENARIO}.csv")
with open(nome_tempo, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_tempo) + "\n")
print(f"\nTempos salvos em: {nome_tempo}")

linhas_mem = [cabecalho] + [",".join(str(m) for m in linha) for linha in resultados_memoria]
nome_mem = os.path.join("docs", f"resultado-{CENARIO}-memoria.csv")
with open(nome_mem, "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_mem) + "\n")
print(f"Memória salva em: {nome_mem}")

if desativados:
    print(f"\nAlgoritmos desativados por timeout: {', '.join(sorted(desativados))}")
    print("Seus valores no CSV estão marcados como -1 (timeout) ou -2 (pulado).")