import csv
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Configurações
GRAU_MAX = 2                # tenta quadrático; cai para linear se parábola abrir para baixo
SALVAR   = True
PASTA_SAIDA = os.path.join("docs", "graficos")
EXTRAPOLAR  = [2, 3, 4]     # 2×, 3×, 4× o maior vetor analisado
T_BASE = 10_000             # deve coincidir com T no experimento.py

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

# Leitura dos CSVs
def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    result = {}
    for col in rows[0]:
        result[col] = np.array([
            np.nan if int(r[col]) < 0 else float(r[col]) for r in rows
        ])
    return len(rows), result

dados    = {}
n_linhas = {}

for cenario, caminho in CENARIOS.items():
    if os.path.exists(caminho):
        n, d = ler_csv(caminho)
        dados[cenario]    = d
        n_linhas[cenario] = n
    else:
        print(f"⚠  {caminho} não encontrado — cenário '{cenario}' ignorado.")

if not dados:
    raise SystemExit("Nenhum CSV em docs/. Rode experimento.py primeiro.")

algoritmos          = list(next(iter(dados.values())).keys())
cenarios_presentes  = list(dados.keys())

def x_para_cenario(cenario):
    return np.array([T_BASE * i for i in range(1, n_linhas[cenario] + 1)])

X_MAX_GLOBAL = max(T_BASE * n for n in n_linhas.values())


# Regressão com grau adaptativo
def ajustar(X, y):
    """
    Ajusta polinômio ignorando NaN.
    - Normaliza X internamente para estabilidade numérica.
    - Começa com grau 2; se o coeficiente de x² for negativo
        (parábola para baixo — fisicamente impossível para tempo),
        cai para grau 1 (linear).
    Retorna (callable p(x_orig), coefs_na_escala_original, grau_usado).
    """
    mascara = ~np.isnan(y)
    if mascara.sum() < 2:
        return None, None, None

    X_m = X.mean()
    X_s = X.std() if X.std() > 0 else 1.0
    Xn  = (X[mascara] - X_m) / X_s
    yn  = y[mascara]

    def _fit(grau):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", Warning)
            return np.polyfit(Xn, yn, grau)

    coefs_norm = _fit(GRAU_MAX)
    grau_usado = GRAU_MAX

    # Se o polinômio de grau 2 abre para baixo → usa grau 1
    # O coef de maior grau no espaço normalizado determina a abertura
    if GRAU_MAX == 2 and coefs_norm[0] < 0:
        coefs_norm = _fit(1)
        grau_usado = 1

    p_norm = np.poly1d(coefs_norm)

    def p(x_orig):
        return p_norm((np.asarray(x_orig, dtype=float) - X_m) / X_s)

    # Coeficientes na escala original (para exibir na equação)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", Warning)
        coefs_orig = np.polyfit(X[mascara], yn, grau_usado)

    return p, coefs_orig, grau_usado


def r_quadrado(X, y, p):
    mascara = ~np.isnan(y)
    y_obs  = y[mascara]
    y_fit  = np.array([p(xi) for xi in X[mascara]])
    ss_res = np.sum((y_obs - y_fit) ** 2)
    ss_tot = np.sum((y_obs - y_obs.mean()) ** 2)
    return 1.0 if ss_tot == 0 else 1 - ss_res / ss_tot


def formatar_equacao(coefs, grau):
    simbolos = ["x²", "x", ""] if grau == 2 else ["x", ""]
    # garante que coefs tem exatamente grau+1 elementos
    coefs = list(coefs)
    termos = []
    for c, sim in zip(coefs, simbolos):
        if abs(c) < 1e-15:
            continue
        termos.append(f"{c:.4g}{sim}")
    eq = " + ".join(termos).replace("+ -", "− ")
    return f"f(x) = {eq}"


def ms_para_str(ms):
    if ms <= 0:
        return "< 1 ms"
    if ms < 1_000:
        return f"{ms:.0f} ms"
    if ms < 60_000:
        return f"{ms/1_000:.1f} s"
    return f"{ms/60_000:.1f} min"


# Geração dos gráficos individuais
if SALVAR:
    os.makedirs(PASTA_SAIDA, exist_ok=True)

X_ext_max = X_MAX_GLOBAL * max(EXTRAPOLAR)
X_curva   = np.linspace(T_BASE, X_ext_max, 600)

for alg in algoritmos:
    fig = plt.figure(figsize=(11, 6))
    gs  = gridspec.GridSpec(1, 2, width_ratios=[2.5, 1], figure=fig)
    ax     = fig.add_subplot(gs[0])
    ax_tab = fig.add_subplot(gs[1])
    ax_tab.axis("off")

    ax.set_title(ROTULOS.get(alg, alg), fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Tamanho da entrada (n)", fontsize=11)
    ax.set_ylabel("Tempo (ms)", fontsize=11)

    texto_bloco = []
    previsoes_por_mult = {m: [] for m in EXTRAPOLAR}
    tem_dados = False

    for cenario in cenarios_presentes:
        X   = x_para_cenario(cenario)
        y   = dados[cenario][alg]
        cor = CORES[cenario]
        p, coefs, grau = ajustar(X, y)

        if p is None:
            texto_bloco.append(f"[{cenario}]  sem dados válidos")
            for m in EXTRAPOLAR:
                previsoes_por_mult[m].append("—")
            continue

        tem_dados = True
        mascara   = ~np.isnan(y)
        r2        = r_quadrado(X, y, p)

        y_curva = np.array([p(xi) for xi in X_curva])

        ax.scatter(X[mascara], y[mascara], color=cor, s=30, zorder=4, alpha=0.9)
        ax.plot(X_curva, y_curva, color=cor, linewidth=2,
                linestyle="--", label=cenario, alpha=0.9)

        eq_str = formatar_equacao(coefs, grau)
        grau_str = "quad." if grau == 2 else "linear"
        texto_bloco.append(f"[{cenario}]  {eq_str}   R²={r2:.4f}  ({grau_str})")

        for m in EXTRAPOLAR:
            val = p(X_MAX_GLOBAL * m)
            previsoes_por_mult[m].append(ms_para_str(val))

    # Linha divisória observado / extrapolado
    ax.axvline(X_MAX_GLOBAL, color="black", linestyle="--", linewidth=0.8, alpha=0.4)
    ylim = ax.get_ylim()
    ax.text(X_MAX_GLOBAL * 1.01, ylim[1] * 0.97,
            "← observado  |  extrapolado →",
            fontsize=7.5, color="gray", ha="left", va="top")

    for m in EXTRAPOLAR:
        ax.axvline(X_MAX_GLOBAL * m, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
        ax.text(X_MAX_GLOBAL * m, ylim[1] * 0.97, f"{m}×", fontsize=7, color="gray", ha="center")

    ax.text(
            0.02, 0.98, "\n".join(texto_bloco),
            transform=ax.transAxes, fontsize=8, verticalalignment="top",
            fontfamily="monospace",
            bbox=dict(
                    boxstyle="round,pad=0.4", facecolor="white", edgecolor="#cccccc", alpha=0.88
                )
        )

    handles = [
            plt.Line2D(
                    [0], [0], color=CORES[c], linewidth=2,
                    linestyle="--", marker="o", markersize=5, label=c
                )
            for c in cenarios_presentes
        ]
    ax.legend(handles=handles, fontsize=10, loc="upper left", bbox_to_anchor=(0.02, 0.72))
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.set_xlim(T_BASE * 0.8, X_ext_max * 1.02)

    # Tabela de previsões
    if tem_dados:
        cab = ["Vetor (n)"] + [c.capitalize() for c in cenarios_presentes]
        linhas_tab = []
        for m in EXTRAPOLAR:
            n_fmt = f"{int(X_MAX_GLOBAL * m):,}"
            linhas_tab.append([f"{m}× ({n_fmt})"] + previsoes_por_mult[m])

        tbl = ax_tab.table(cellText=linhas_tab, colLabels=cab, loc="center", cellLoc="center")
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(9.5)
        tbl.scale(1, 2.0)
        for j in range(len(cab)):
            tbl[0, j].set_facecolor("#1A3260")
            tbl[0, j].set_text_props(color="white", fontweight="bold")
        for i in range(1, len(linhas_tab) + 1):
            for j in range(len(cab)):
                tbl[i, j].set_facecolor("#F0F4FF" if i % 2 == 0 else "white")
        ax_tab.set_title("Previsão por regressão", fontsize=10, fontweight="bold", pad=8)
    else:
        ax_tab.text(
                0.5, 0.5, "Sem dados\n(timeout em\ntodos os cenários)",
                ha="center", va="center", fontsize=10, color="gray",
                transform=ax_tab.transAxes
            )

    plt.tight_layout()
    if SALVAR:
        caminho_png = os.path.join(PASTA_SAIDA, f"{alg}.png")
        fig.savefig(caminho_png, dpi=150, bbox_inches="tight")
        print(f"  Salvo: {caminho_png}")
    plt.show()
    plt.close(fig)


# Painel resumo
n_alg  = len(algoritmos)
n_cols = 5
n_rows = (n_alg + n_cols - 1) // n_cols

fig_res, axes = plt.subplots(n_rows, n_cols,
                              figsize=(n_cols * 4, n_rows * 3.2))
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

    for cenario in cenarios_presentes:
        X   = x_para_cenario(cenario)
        y   = dados[cenario][alg]
        cor = CORES[cenario]
        p, coefs, grau = ajustar(X, y)
        if p is None:
            continue
        mascara = ~np.isnan(y)
        r2      = r_quadrado(X, y, p)
        ax.scatter(X[mascara], y[mascara], color=cor, s=8, alpha=0.7, zorder=3)
        ax.plot(X_curva, [p(xi) for xi in X_curva], color=cor, linewidth=1.4,
                linestyle="--", label=f"{cenario} R²={r2:.3f}")

    ax.axvline(X_MAX_GLOBAL, color="black", linestyle="--", linewidth=0.6, alpha=0.3)
    ax.legend(fontsize=6, loc="upper left", framealpha=0.7)
    ax.grid(True, linestyle=":", alpha=0.3)

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