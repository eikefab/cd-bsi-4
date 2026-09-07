from textwrap import fill

import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MaxNLocator


VALORES = ["valor_declarado", "valor_venda"]


def histograma_valor_venda(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(df["valor_venda"].dropna(), bins=5, rwidth=0.85)
    ax.set(
        title="Distribuição dos preços de venda",
        xlabel="Valor de venda (R$)", ylabel="Quantidade de registros",
    )

    return fig


def evolucao_preco(df):
    frequencias = df["descricao"].value_counts()

    if frequencias.empty:
        return None

    descricao = frequencias.index[0]
    produto = df.loc[df["descricao"].eq(descricao)].dropna(
        subset=["data_venda", "valor_venda"]
    )

    if produto.empty:
        return None

    precos = produto.groupby(produto["data_venda"].dt.normalize())["valor_venda"].median()
    precos = precos.sort_index().asfreq("D")

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(precos.index, precos, marker="o")
    ax.set(
        title=f"Evolução do preço — mediana diária\n{fill(descricao, width=60)}",
        xlabel="Data (horário de São Paulo)",
        ylabel="Valor de venda (R$)",
    )

    ax.xaxis.set_major_locator(AutoDateLocator(tz=precos.index.tz, interval_multiples=False))
    ax.xaxis.set_major_formatter(DateFormatter("%d/%m/%Y", tz=precos.index.tz))

    fig.autofmt_xdate()

    return fig


def dispersao_valores(df):
    pares = df.dropna(subset=VALORES)

    if pares.empty:
        return None

    fig, ax = plt.subplots(figsize=(9, 7))

    ax.scatter(pares["valor_declarado"], pares["valor_venda"])

    minimo = pares[VALORES].min().min()
    maximo = pares[VALORES].max().max()

    ax.plot(
        [minimo, maximo], [minimo, maximo], "--",
        label="Valores iguais",
    )

    ax.set(
        title="Valor declarado e valor de venda por registro",
        xlabel="Valor declarado (R$)", ylabel="Valor de venda (R$)",
    )

    ax.legend()

    return fig


def boxplot_por_descricao(df):
    produtos = df.dropna(subset=["descricao", "valor_venda"])
    frequencias = produtos["descricao"].value_counts().head(10)

    if frequencias.empty:
        return None

    linhas = (len(frequencias) + 1) // 2

    fig, eixos = plt.subplots(
        linhas, 2, figsize=(14, linhas * 2.5 + 1),
        squeeze=False, layout="constrained",
    )

    fig.suptitle(
        "Variação de preço por descrição\n"
        "Dez descrições mais frequentes · escalas independentes em R$ · todos os extremos visíveis",
    )

    for ax, (descricao, quantidade) in zip(eixos.flat, frequencias.items()):
        grupo = produtos.loc[produtos["descricao"].eq(descricao), "valor_venda"]

        ax.boxplot([grupo], tick_labels=[""], orientation="horizontal")

        ax.set_title(fill(descricao, width=53))
        ax.set_xlabel(
            f"Valor (R$) · n = {quantidade} · Mediana R$ {grupo.median():.2f}",
        )

        ax.xaxis.set_major_locator(MaxNLocator(4))
        
        ax.margins(x=0.15)

    for ax in list(eixos.flat)[len(frequencias):]:
        ax.set_visible(False)

    return fig
