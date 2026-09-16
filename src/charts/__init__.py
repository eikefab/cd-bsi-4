from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from .files import salva_grafico
from .plots import (
    GRUPOS,
    GRUPOS_SPRAY_METALICA,
    GRUPOS_TINTAS,
    boxplot_precos_por_grupos,
    histograma_kde_por_grupo,
)


ARQUIVOS_LEGADOS = {
    "histograma_valor_venda.png",
    "dispersao_valores.png",
    "boxplot_por_descricao.png",
    "evolucao_preco.png",
}


def carrega_dados(csv_file):
    df = pd.read_csv(csv_file)
    campos = ["grupo", "valor_venda"]
    ausentes = [campo for campo in campos if campo not in df.columns]
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(ausentes)}")

    df["grupo"] = df["grupo"].astype("string").str.strip()
    df["valor_venda"] = pd.to_numeric(df["valor_venda"], errors="coerce")
    df["valor_venda"] = df["valor_venda"].replace(
        [float("inf"), -float("inf")], float("nan")
    )

    if df["valor_venda"].isna().all():
        raise ValueError("O CSV precisa conter preços de venda numéricos.")

    return df


def nomes_arquivos_gerenciados():
    nomes = ARQUIVOS_LEGADOS | {
        "boxplot_precos_por_grupo.png",
        "boxplot_precos_tintas.png",
        "boxplot_precos_spray_metalica.png",
    }
    for grupo in GRUPOS:
        nomes.add(f"histograma_{grupo}.png")
        nomes.add(f"kde_{grupo}.png")
        nomes.add(f"distribuicao_{grupo}.png")
    return nomes


def remove_graficos_anteriores(output_folder):
    for nome in nomes_arquivos_gerenciados():
        (output_folder / nome).unlink(missing_ok=True)


def generate_charts(csv_file="output/silver.csv", output_folder="output/charts"):
    df = carrega_dados(csv_file)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    remove_graficos_anteriores(output_folder)

    arquivos = []

    boxplots = [
        (
            GRUPOS_TINTAS,
            "Distribuição dos preços - tintas branca e acrílicas",
            "boxplot_precos_tintas.png",
            None,
        ),
        (
            GRUPOS_SPRAY_METALICA,
            "Distribuição dos preços - tintas spray e metálica",
            "boxplot_precos_spray_metalica.png",
            10,
        ),
    ]
    for grupos, titulo, nome, intervalo_eixo_x in boxplots:
        fig = boxplot_precos_por_grupos(
            df, grupos, titulo, intervalo_eixo_x=intervalo_eixo_x
        )
        if fig is not None:
            arquivos.append(salva_grafico(fig, output_folder, nome))

    for grupo in GRUPOS:
        fig = histograma_kde_por_grupo(df, grupo)
        if fig is not None:
            arquivos.append(
                salva_grafico(fig, output_folder, f"distribuicao_{grupo}.png")
            )

    return arquivos
