import pandas as pd


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

    df = df.drop_duplicates()

    bad_words = ["tecidos", "tecido", "coador", "promocao", "promoçao", "promoção"]
    for word in bad_words:
        df = df[~df["descricao"].str.contains(word, case=False, na=False)]

    df = df.drop(columns=["descricao_sefaz", "unidade_medida", "gtin", "ncm", "gpc"])
    df = df.sort_values(by=["descricao"], ascending=[True])

    return df
    
def normaliza_descricao_por_campo(df, campo):
    chave = df[campo].astype("string").str.strip()
    descricao = (
        df["descricao"]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    grupos_validos = (
        chave.notna()
        & chave.ne("")
        & chave.duplicated(keep=False)
    )

    descricao_do_grupo = descricao.groupby(chave).transform("first")

    df.loc[grupos_validos, "descricao"] = descricao_do_grupo.loc[grupos_validos]

    return df


