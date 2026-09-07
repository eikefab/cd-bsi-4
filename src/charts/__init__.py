from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")

from .plots import (
    VALORES,
    boxplot_por_descricao,
    dispersao_valores,
    evolucao_preco,
    histograma_valor_venda,
)
from .files import salva_grafico


GRAFICOS = [
    (histograma_valor_venda, "histograma_valor_venda.png"),
    (dispersao_valores, "dispersao_valores.png"),
    (boxplot_por_descricao, "boxplot_por_descricao.png"),
    (evolucao_preco, "evolucao_preco.png"),
]


def carrega_dados(csv_file):
    df = pd.read_csv(csv_file)
    campos = ["descricao", "data_venda", *VALORES]
    ausentes = [campo for campo in campos if campo not in df.columns]
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(ausentes)}")

    for campo in VALORES:
        df[campo] = pd.to_numeric(df[campo], errors="coerce")
        df[campo] = df[campo].replace([float("inf"), -float("inf")], float("nan"))

    if df[VALORES].isna().all().any():
        raise ValueError("O CSV precisa conter valores numéricos declarados e de venda.")

    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce", utc=True)
    df["data_venda"] = df["data_venda"].dt.tz_convert("America/Sao_Paulo")
    return df


def generate_charts(csv_file="output/silver.csv", output_folder="output/charts"):
    df = carrega_dados(csv_file)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    arquivos = []
    for criar_grafico, nome in GRAFICOS:
        fig = criar_grafico(df)
        if fig is not None:
            arquivos.append(salva_grafico(fig, output_folder, nome))
    return arquivos
