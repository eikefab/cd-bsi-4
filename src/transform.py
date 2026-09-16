import pandas as pd


UNIDADES_PADRONIZADAS = {
    "UND": "UN",
    "un": "UN",
    "UNI": "UN",
    "UNID": "UN",
    "UNIDA": "UN",
    "UN0001": "UN",
    "Un": "UN",
    "LT": "L",
    "LITRO": "L",
}

PADRAO_BRANCA = r"\b(?:branca|branco|br)\b"
PADRAO_ACRILICA = r"\bacr\w*\b"
PADRAO_SPRAY = r"\b(?:spray|spra|spr|aerossol|aerosol|aer)\b"
PADRAO_METALICA = r"\b(?:met\w*|met\.)"
PADRAO_ACABAMENTO_METALICO = (
    r"\b(?:alum\w*|prata|crom\w*|dour\w*|ouro|bronze|cobre)\b"
)

COLUNAS_SAIDA = [
    "codigo",
    "descricao",
    "unidade_medida",
    "grupo",
    "data_venda",
    "valor_declarado",
    "valor_venda",
]


def transform_data(csv_file):
    df = pd.read_csv(csv_file)

    df = df.dropna(how="all")

    df = normaliza_descricao_por_campo(df, "descricao_sefaz")
    df = normaliza_descricao_por_campo(df, "codigo")

    df["descricao"] = (
        df["descricao"]
        .astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"""[*"'“”„‟‘’‚‛`]""", "", regex=True)
    )

    df["unidade_medida"] = df["unidade_medida"].replace(UNIDADES_PADRONIZADAS)
    df = df.drop_duplicates()

    bad_words = ["tecidos", "tecido", "coador", "promocao", "promoçao", "promoção"]
    for word in bad_words:
        df = df[~df["descricao"].str.contains(word, case=False, na=False)]

    df = agrupa_tintas(df)

    df = df.drop(columns=["descricao_sefaz", "gtin", "ncm", "gpc"])
    df = df[COLUNAS_SAIDA]
    df = df.sort_values(by=["descricao", "grupo"], kind="stable")

    return df.reset_index(drop=True)


def agrupa_tintas(df):
    descricao = df["descricao"].astype("string")

    tinta_branca = descricao.str.contains(
        PADRAO_BRANCA, case=False, na=False, regex=True
    )
    tinta_acrilica = descricao.str.contains(
        PADRAO_ACRILICA, case=False, na=False, regex=True
    )
    tinta_spray = descricao.str.contains(
        PADRAO_SPRAY, case=False, na=False, regex=True
    )
    tinta_metalica = descricao.str.contains(
        PADRAO_METALICA, case=False, na=False, regex=True
    )
    acabamento_metalico = descricao.str.contains(
        PADRAO_ACABAMENTO_METALICO, case=False, na=False, regex=True
    )
    tinta_metalica = tinta_metalica | (tinta_spray & acabamento_metalico)

    grupos = [
        ("tinta_branca", tinta_branca),
        ("tinta_acrilica_branca", tinta_acrilica & tinta_branca),
        ("tinta_acrilica", tinta_acrilica),
        ("tinta_spray", tinta_spray),
        ("tinta_metalica", tinta_metalica),
    ]

    dataframes = []
    for nome, mascara in grupos:
        grupo = df.loc[mascara].copy()
        grupo["grupo"] = nome
        dataframes.append(grupo)

    return pd.concat(dataframes, ignore_index=True)


def normaliza_descricao_por_campo(df, campo):
    chave = df[campo].astype("string").str.strip()
    descricao = df["descricao"].astype("string").str.strip().replace("", pd.NA)

    grupos_validos = chave.notna() & chave.ne("") & chave.duplicated(keep=False)

    descricao_do_grupo = descricao.groupby(chave).transform("first")

    df.loc[grupos_validos, "descricao"] = descricao_do_grupo.loc[grupos_validos]

    return df
