import math

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import FuncFormatter, MaxNLocator, MultipleLocator, PercentFormatter

from ..report import format_currency, format_modes, summarize_prices


GRUPOS = {
    "tinta_branca": {
        "rotulo": "Tinta branca",
        "cor": "#4C78A8",
    },
    "tinta_acrilica_branca": {
        "rotulo": "Tinta acrílica branca",
        "cor": "#F58518",
    },
    "tinta_acrilica": {
        "rotulo": "Tinta acrílica",
        "cor": "#54A24B",
    },
    "tinta_spray": {
        "rotulo": "Tinta spray",
        "cor": "#E45756",
    },
    "tinta_metalica": {
        "rotulo": "Tinta metálica",
        "cor": "#B279A2",
    },
}

GRUPOS_TINTAS = (
    "tinta_branca",
    "tinta_acrilica_branca",
    "tinta_acrilica",
)

GRUPOS_SPRAY_METALICA = (
    "tinta_spray",
    "tinta_metalica",
)


def precos_do_grupo(df, grupo):
    return df.loc[df["grupo"].eq(grupo), "valor_venda"].dropna()


def formata_preco(valor):
    if math.isclose(valor, round(valor)):
        return f"{valor:.0f}"
    return f"{valor:.2f}".replace(".", ",")


def boxplot_precos_por_grupos(df, grupos, titulo, intervalo_eixo_x=None):
    dados = []
    rotulos = []
    cores = []

    for grupo in grupos:
        configuracao = GRUPOS[grupo]
        precos = precos_do_grupo(df, grupo)
        if precos.empty:
            continue

        dados.append(precos)
        rotulos.append(f"{configuracao['rotulo']} (n={len(precos)})")
        cores.append(configuracao["cor"])

    if not dados:
        return None

    fig, ax = plt.subplots(figsize=(11, 7), layout="constrained")
    elementos = ax.boxplot(
        dados,
        tick_labels=rotulos,
        orientation="horizontal",
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 1.5},
    )

    for caixa, cor in zip(elementos["boxes"], cores):
        caixa.set_facecolor(cor)
        caixa.set_alpha(0.75)

    ax.set(
        title=titulo,
        xlabel="Valor de venda (R$)",
        ylabel="Grupo",
    )
    ax.invert_yaxis()
    if intervalo_eixo_x is not None:
        ax.xaxis.set_major_locator(MultipleLocator(intervalo_eixo_x))
    ax.grid(axis="x", linestyle=":", alpha=0.4)

    return fig


def histograma_kde_por_grupo(df, grupo):
    precos = precos_do_grupo(df, grupo)
    if precos.empty:
        return None

    configuracao = GRUPOS[grupo]
    resumo = summarize_prices(precos)
    limite = precos.quantile(0.95)
    precos_centrais = precos[precos <= limite]
    fora_do_detalhe = len(precos) - len(precos_centrais)

    fig = plt.figure(figsize=(15, 7), layout="constrained")
    grade = fig.add_gridspec(2, 2, height_ratios=(6, 1))
    ax_completo = fig.add_subplot(grade[0, 0])
    ax_detalhe = fig.add_subplot(grade[0, 1])
    ax_tabela = fig.add_subplot(grade[1, :])
    fig.suptitle(f"Distribuição dos preços — {configuracao['rotulo']} (n={len(precos)})")

    sns.histplot(
        x=precos,
        bins="auto",
        kde=precos.nunique() > 1,
        stat="percent",
        color=configuracao["cor"],
        edgecolor="white",
        alpha=0.5,
        kde_kws={"cut": 0, "clip": (precos.min(), precos.max())},
        line_kws={"linewidth": 2},
        ax=ax_completo,
    )
    ax_detalhe.hist(
        precos_centrais,
        bins=np.histogram_bin_edges(precos_centrais, bins="auto"),
        weights=np.full(len(precos_centrais), 100 / len(precos)),
        color=configuracao["cor"],
        edgecolor="white",
        alpha=0.7,
    )
    if not math.isclose(precos.min(), limite):
        ax_detalhe.set_xlim(precos.min(), limite)

    for ax in (ax_completo, ax_detalhe):
        ax.set(xlabel="Valor de venda (R$)", ylabel="Percentual do grupo (%)")
        ax.xaxis.set_major_locator(MaxNLocator(nbins=7))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda valor, _: formata_preco(valor)))
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))
        ax.grid(axis="y", linestyle=":", alpha=0.4)

    ax_completo.set_title("Visão completa")
    ax_detalhe.set_title(
        f"Detalhe até P95 ({format_currency(limite)}) — "
        f"{fora_do_detalhe} registro(s) acima"
    )

    ax_tabela.axis("off")
    tabela = ax_tabela.table(
        cellText=[[
            format_currency(resumo["mean"]),
            format_currency(resumo["median"]),
            format_modes(resumo),
        ]],
        colLabels=[
            "Média",
            "Mediana",
            f"Moda (frequência: {resumo['frequency']})" if resumo["modes"] else "Moda",
        ],
        cellLoc="center",
        loc="center",
        bbox=(0.08, 0.02, 0.84, 0.96),
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    for cell in tabela.get_celld().values():
        cell.get_text().set_parse_math(False)

    return fig
