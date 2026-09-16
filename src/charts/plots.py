import math

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator, PercentFormatter


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


def marcacoes_eixo_precos(valor_minimo, valor_maximo, intervalo=5):
    marcacoes = [valor_minimo]
    valor = math.ceil(valor_minimo / intervalo) * intervalo

    while valor < valor_maximo:
        distante_dos_limites = (
            valor - valor_minimo >= intervalo / 2
            and valor_maximo - valor >= intervalo / 2
        )
        if distante_dos_limites:
            marcacoes.append(valor)
        valor += intervalo

    if not math.isclose(valor_minimo, valor_maximo):
        marcacoes.append(valor_maximo)

    return marcacoes


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
    valor_minimo = precos.min()
    valor_maximo = precos.max()
    marcacoes = marcacoes_eixo_precos(valor_minimo, valor_maximo)
    largura = min(30, max(10, len(marcacoes) * 0.22))

    fig, ax = plt.subplots(figsize=(largura, 7), layout="constrained")
    sns.histplot(
        x=precos,
        bins="auto",
        kde=True,
        stat="percent",
        color=configuracao["cor"],
        edgecolor="white",
        alpha=0.4,
        kde_kws={"cut": 0, "clip": (valor_minimo, valor_maximo)},
        line_kws={"linewidth": 2},
        ax=ax,
    )
    ax.set(
        title=f"Histograma e KDE - {configuracao['rotulo']} (n={len(precos)})",
        xlabel="Valor de venda (R$)",
        ylabel="Percentual do grupo (%)",
    )
    ax.set_xlim(valor_minimo, valor_maximo)
    ax.set_xticks(marcacoes, labels=[formata_preco(valor) for valor in marcacoes])
    ax.tick_params(axis="x", labelrotation=90, labelsize=7)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100))
    ax.grid(axis="y", linestyle=":", alpha=0.4)

    return fig
