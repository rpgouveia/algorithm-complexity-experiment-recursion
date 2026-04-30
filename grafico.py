import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Configurações
GRAU = 2          # grau do polinômio de regressão (2 = quadrático)
SALVAR = True     # True: salva PNGs em docs/graficos/  |  False: só exibe
PASTA_SAIDA = os.path.join("docs", "graficos")

CENARIOS = {
    "crescente":   "docs/resultado-crescente.csv",
    "decrescente": "docs/resultado-decrescente.csv",
    "random":      "docs/resultado-random.csv",
}

CORES = {
    "crescente":   "#1D9E75",
    "decrescente": "#E24B4A",
    "random":      "#378ADD",
}

ROTULOS = {
    "QS1":       "QS1 – Quick Sort (trad.)",
    "QS2":       "QS2 – Quick Sort (rand.)",
    "MS1":       "MS1 – Merge Sort (iter.)",
    "MS2":       "MS2 – Merge Sort (rec.)",
    "MS3":       "MS3 – Merge Sort (rand.)",
    "SS1":       "SS1 – Selection Sort (rec.)",
    "SS2":       "SS2 – Selection Sort (rand.)",
    "BASE_LINE": "Shell Sort (baseline)",
    "IS1":       "IS1 – Insertion Sort (iter.)",
    "IS2":       "IS2 – Insertion Sort (rec.)",
}

X = np.array([250 * i for i in range(1, 21)])

# Leitura dos CSVs
def ler_csv(caminho):
    """Lê um CSV e retorna dict {coluna: [valores]}."""
    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return {col: np.array([int(row[col]) for row in rows]) for col in rows[0]}

dados = {}
for cenario, caminho in CENARIOS.items():
    if os.path.exists(caminho):
        dados[cenario] = ler_csv(caminho)
    else:
        print(f"⚠  Arquivo não encontrado: {caminho} — cenário '{cenario}' ignorado.")

if not dados:
    raise SystemExit("Nenhum CSV encontrado em docs/. Rode experimento.py primeiro.")

algoritmos = list(next(iter(dados.values())).keys())

# Funções auxiliares
def r_quadrado(y, y_fit):
    """Calcula o coeficiente de determinação R²."""
    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot if ss_tot != 0 else 1.0

def formatar_equacao(coefs, grau):
    """
    Recebe os coeficientes do polinômio (ordem decrescente) e retorna
    uma string formatada estilo Excel: f(x) = ax² + bx + c
    """
    termos = []
    for exp, c in zip(range(grau, -1, -1), coefs):
        if abs(c) < 1e-12:
            continue
        c_fmt = f"{c:.4g}"
        if exp == 0:
            termos.append(c_fmt)
        elif exp == 1:
            termos.append(f"{c_fmt}x")
        else:
            termos.append(f"{c_fmt}x²" if exp == 2 else f"{c_fmt}x^{exp}")
    eq = " + ".join(termos).replace("+ -", "− ")
    return f"f(x) = {eq}"

# Geração dos gráficos — um por algoritmo
if SALVAR:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

X_ext = np.linspace(X[0], X[-1], 300)   # curva suave para plotar a regressão

for alg in algoritmos:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_title(ROTULOS.get(alg, alg), fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Tamanho da entrada (n)", fontsize=11)
    ax.set_ylabel("Tempo (ms)", fontsize=11)

    cenarios_presentes = [c for c in CENARIOS if c in dados]
    anotacoes = []   # (x_ancora, y_ancora, texto, cor)

    for cenario in cenarios_presentes:
        y = dados[cenario][alg]
        cor = CORES[cenario]

        # Pontos de dados
        ax.scatter(X, y, color=cor, s=22, zorder=3, alpha=0.85)

        # Regressão polinomial
        coefs = np.polyfit(X, y, GRAU)
        p = np.poly1d(coefs)
        y_fit = p(X)
        r2 = r_quadrado(y, y_fit)

        # Curva suavizada
        ax.plot(X_ext, p(X_ext), color=cor, linewidth=2,
                label=cenario, linestyle="--", alpha=0.9)

        eq_str = formatar_equacao(coefs, GRAU)
        anotacoes.append((cenario, eq_str, r2, cor))

    # Bloco de texto com equações e R² (canto superior esquerdo)
    texto_bloco = []
    for cenario, eq, r2, _ in anotacoes:
        texto_bloco.append(f"[{cenario}]  {eq}   R² = {r2:.4f}")

    ax.text(
            0.02, 0.98, "\n".join(texto_bloco),
            transform=ax.transAxes,
            fontsize=8.5, verticalalignment="top",
            fontfamily="monospace",
            bbox=dict(
                    boxstyle="round,pad=0.4", facecolor="white",
                    edgecolor="#cccccc", alpha=0.85
                )
        )

    # Legenda lateral
    handles = [
        plt.Line2D(
                [0], [0], 
                color=CORES[c], 
                linewidth=2, 
                linestyle="--",
                marker="o", 
                markersize=5, 
                label=c
            )
        for c in cenarios_presentes
    ]
    ax.legend(handles=handles, fontsize=10, loc="lower right")
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.set_xlim(X[0] - 100, X[-1] + 100)

    plt.tight_layout()

    if SALVAR:
        caminho_png = os.path.join(PASTA_SAIDA, f"{alg}.png")
        fig.savefig(caminho_png, dpi=150, bbox_inches="tight")
        print(f"  Salvo: {caminho_png}")

    plt.show()
    plt.close(fig)

# Painel resumo — todos os algoritmos em grid
n_alg = len(algoritmos)
n_cols = 5
n_rows = (n_alg + n_cols - 1) // n_cols

fig_res, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4, n_rows * 3.2))
fig_res.suptitle(
    "Complexidade de Algoritmos de Ordenação — Resumo",
    fontsize=14, fontweight="bold", y=1.01
)
axes_flat = axes.flatten()

for idx, alg in enumerate(algoritmos):
    ax = axes_flat[idx]
    ax.set_title(ROTULOS.get(alg, alg), fontsize=8, fontweight="bold")
    ax.set_xlabel("n", fontsize=7)
    ax.set_ylabel("ms", fontsize=7)
    ax.tick_params(labelsize=7)

    for cenario in [c for c in CENARIOS if c in dados]:
        y = dados[cenario][alg]
        cor = CORES[cenario]
        coefs = np.polyfit(X, y, GRAU)
        p = np.poly1d(coefs)
        r2 = r_quadrado(y, p(X))
        ax.scatter(X, y, color=cor, s=8, alpha=0.7, zorder=3)
        ax.plot(X_ext, p(X_ext), color=cor, linewidth=1.4,
                linestyle="--", label=f"{cenario} R²={r2:.3f}")

    ax.legend(fontsize=6, loc="upper left", framealpha=0.7)
    ax.grid(True, linestyle=":", alpha=0.3)

# Esconde subplots vazios
for idx in range(len(algoritmos), len(axes_flat)):
    axes_flat[idx].set_visible(False)

plt.tight_layout()

if SALVAR:
    caminho_resumo = os.path.join(PASTA_SAIDA, "resumo.png")
    fig_res.savefig(caminho_resumo, dpi=150, bbox_inches="tight")
    print(f"\n  Painel resumo salvo: {caminho_resumo}")

plt.show()
plt.close(fig_res)

print("\nConcluído.")