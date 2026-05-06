import csv
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Configurações
GRAU_MAX = 2      
SALVAR   = True
PASTA_SAIDA = os.path.join("docs", "graficos")
EXTRAPOLAR  = [2, 3, 4]   
T_BASE = 10_000            

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


# Funções Auxiliares e Estatística
def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    result = {}
    for col in rows[0]:
        result[col] = np.array([
            np.nan if int(r[col]) < 0 else float(r[col]) for r in rows
        ])
    return len(rows), result

def ajustar(X, y):
    mascara = ~np.isnan(y)
    if mascara.sum() < 2: return None, None, None
    X_m, X_s = X.mean(), (X.std() if X.std() > 0 else 1.0)
    Xn, yn = (X[mascara] - X_m) / X_s, y[mascara]
    def _fit(grau):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", Warning)
            return np.polyfit(Xn, yn, grau)
    coefs_norm = _fit(GRAU_MAX)
    grau_usado = GRAU_MAX
    if GRAU_MAX == 2 and coefs_norm[0] < 0:
        coefs_norm = _fit(1)
        grau_usado = 1
    p_norm = np.poly1d(coefs_norm)
    def p(x_orig): return p_norm((np.asarray(x_orig, dtype=float) - X_m) / X_s)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", Warning)
        coefs_orig = np.polyfit(X[mascara], yn, grau_usado)
    return p, coefs_orig, grau_usado

def r_quadrado(X, y, p):
    mascara = ~np.isnan(y)
    y_obs, y_fit = y[mascara], np.array([p(xi) for xi in X[mascara]])
    ss_res = np.sum((y_obs - y_fit) ** 2)
    ss_tot = np.sum((y_obs - y_obs.mean()) ** 2)
    return 1.0 if ss_tot == 0 else 1 - ss_res / ss_tot

def formatar_equacao(coefs, grau):
    simbolos = ["x²", "x", ""] if grau == 2 else ["x", ""]
    coefs = list(coefs)
    termos = []
    for c, sim in zip(coefs, simbolos):
        if abs(c) < 1e-15: continue
        termos.append(f"{c:.3g}{sim}")
    eq = " + ".join(termos).replace("+ -", "− ")
    return f"f(x) = {eq}"

def ms_para_str(ms):
    if np.isnan(ms) or ms < 0: return "—"
    if ms < 1_000: return f"{ms:.0f} ms"
    if ms < 60_000: return f"{ms/1_000:.2f} s"
    return f"{ms/60_000:.1f} min"


# Processamento
dados, n_linhas = {}, {}
for cenario, caminho in CENARIOS.items():
    if os.path.exists(caminho):
        n, d = ler_csv(caminho)
        dados[cenario], n_linhas[cenario] = d, n

if not dados: raise SystemExit("Nenhum CSV encontrado.")

algoritmos = list(next(iter(dados.values())).keys())
cenarios_presentes = list(dados.keys())
X_MAX_GLOBAL = max(T_BASE * n for n in n_linhas.values())

if SALVAR: os.makedirs(PASTA_SAIDA, exist_ok=True)

X_ext_max = X_MAX_GLOBAL * max(EXTRAPOLAR)
X_curva = np.linspace(T_BASE, X_ext_max, 600)

for alg in algoritmos:
    fig = plt.figure(figsize=(16, 8))
    fig.patch.set_facecolor('#FAF9F6')
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.8, 1.2], figure=fig)
    ax, ax_tab = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    ax_tab.axis("off")

    ax.set_title(f"Regressão Estatística: {ROTULOS.get(alg, alg)}", fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Tamanho da Entrada (N)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Tempo de Execução", fontsize=11, fontweight="bold")

    texto_estatistico = []
    tem_dados = False
    previsoes = {c: {} for c in cenarios_presentes}

    for cenario in cenarios_presentes:
        X, y, cor = np.array([T_BASE * i for i in range(1, n_linhas[cenario] + 1)]), dados[cenario][alg], CORES[cenario]
        p, coefs, grau = ajustar(X, y)
        if p is None: continue

        tem_dados, mascara = True, ~np.isnan(y)
        r2 = r_quadrado(X, y, p)
        y_curva = np.array([p(xi) for xi in X_curva])

        ax.scatter(X[mascara], y[mascara], color=cor, s=40, zorder=5, alpha=0.9)
        ax.plot(X_curva, y_curva, color=cor, linewidth=2.5, label=cenario.capitalize(), alpha=0.8)

        # Dados para a tabela e bloco de texto
        eq_str = formatar_equacao(coefs, grau)
        texto_estatistico.append(f"{cenario.capitalize()}: {eq_str} | R²={r2:.4f}")
        for m in EXTRAPOLAR: previsoes[cenario][m] = ms_para_str(p(X_MAX_GLOBAL * m))

        # Rótulo de complexidade na ponta da curva
        ax.annotate(f"~ {'O(N²)' if grau == 2 else 'O(N)'}", xy=(X_curva[-1], y_curva[-1]), 
                    xytext=(5, 0), textcoords="offset points", va="center", fontsize=9, fontweight='bold', color=cor)

    # Bloco de Equações e R²
    if texto_estatistico:
        ax.text(0.02, 0.97, "Modelos Matemáticos:\n" + "\n".join(texto_estatistico),
                transform=ax.transAxes, fontsize=9, verticalalignment="top", fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.6", facecolor="white", edgecolor="#2C3E50", alpha=0.9))

    ax.axvline(X_MAX_GLOBAL, color="#333", linestyle="--", linewidth=1, alpha=0.5)
    if tem_dados:
        ax.legend(loc="lower right", frameon=True, shadow=True)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_xlim(0, X_ext_max * 1.05)
    ax.set_ylim(bottom=0)

    # Tabela de Dados e Previsões
    if tem_dados:
        cabecalho = ["N"] + [c.capitalize() for c in cenarios_presentes]
        linhas_tab = []
        for i in range(max(n_linhas.values())):
            n_val = T_BASE * (i + 1)
            lin = [f"{n_val:,}"]
            for c in cenarios_presentes:
                y_arr = dados[c][alg]
                lin.append(ms_para_str(y_arr[i]) if i < len(y_arr) else "—")
            linhas_tab.append(lin)
        
        linhas_tab.append(["PREVISÕES (Regressão)", "", "", ""])
        for m in EXTRAPOLAR:
            linhas_tab.append([f"{m}x ({int(X_MAX_GLOBAL * m):,})"] + [previsoes[c].get(m, "—") for c in cenarios_presentes])

        tbl = ax_tab.table(cellText=linhas_tab, colLabels=cabecalho, loc="center", cellLoc="center")
        tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 2.1)
        for j in range(len(cabecalho)):
            tbl[0, j].set_facecolor("#2C3E50"); tbl[0, j].set_text_props(color="white", fontweight="bold")
        for i in range(1, len(linhas_tab) + 1):
            if "PREVISÕES" in linhas_tab[i-1][0]:
                for j in range(len(cabecalho)): tbl[i, j].set_facecolor("#BDC3C7")
            else:
                for j in range(len(cabecalho)): tbl[i, j].set_facecolor("#F8F9F9" if i % 2 == 0 else "white")
        ax_tab.set_title("Dados Observados e Futuros", fontsize=12, fontweight="bold", pad=20)

    plt.tight_layout()
    if SALVAR: fig.savefig(os.path.join(PASTA_SAIDA, f"{alg}.png"), dpi=180, bbox_inches="tight")
    plt.close(fig)

print("\nGráficos gerados com equações e R² em docs/graficos/")