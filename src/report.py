"""Resumo dos registros e dos preços exibido ao executar o ETL."""

import pandas as pd


GROUP_LABELS = {
    "tinta_branca": "Tinta branca",
    "tinta_acrilica_branca": "Tinta acrílica branca",
    "tinta_acrilica": "Tinta acrílica",
    "tinta_spray": "Tinta spray",
    "tinta_metalica": "Tinta metálica",
}


def summarize_prices(values):
    prices = pd.to_numeric(pd.Series(values), errors="coerce")
    prices = prices.replace([float("inf"), -float("inf")], float("nan")).dropna()
    if prices.empty:
        return {"count": 0, "mean": None, "median": None, "modes": (), "frequency": 0}

    frequencies = prices.round(2).value_counts()
    maximum = int(frequencies.iloc[0])
    modes = tuple(sorted(frequencies[frequencies == maximum].index)) if maximum > 1 else ()
    return {
        "count": len(prices),
        "mean": prices.mean(),
        "median": prices.median(),
        "modes": modes,
        "frequency": maximum if modes else 0,
    }


def format_currency(value):
    if value is None:
        return "—"
    amount = f"{value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {amount}"


def format_modes(summary):
    return "; ".join(format_currency(value) for value in summary["modes"]) or "sem moda"


def print_audit(raw, audit):
    dates = pd.to_datetime(raw["data_venda"], utc=True, errors="coerce").dropna()
    period = f"{dates.min():%d/%m/%Y} a {dates.max():%d/%m/%Y}" if not dates.empty else "indisponível"
    print(f"Período das vendas: {period}")
    print(f"Entrada: {audit['raw_rows']} | vazios: {audit['blank_rows']} | duplicados: {audit['duplicate_rows']}")
    excluded = {word: count for word, count in audit["excluded_counts"].items() if count}
    details = ", ".join(f"{word}: {count}" for word, count in excluded.items()) or "nenhum"
    print(f"Excluídos por descrição: {sum(excluded.values())} ({details})")
    print(
        f"Sem grupo: {audit['unclassified_rows']} | classificados: {audit['classified_rows']} "
        f"| linhas no silver: {sum(audit['group_counts'].values())}"
    )
    counts = [(label, audit["group_counts"].get(group, 0)) for group, label in GROUP_LABELS.items()]
    print("\nGrupos classificados:")
    print(pd.DataFrame(counts, columns=["Grupo", "Registros"]).to_string(index=False))


def print_price_tables(raw, silver):
    def row(label, values):
        summary = summarize_prices(values)
        return (
            label,
            summary["count"],
            format_currency(summary["mean"]),
            format_currency(summary["median"]),
            format_modes(summary),
            summary["frequency"] or "—",
        )

    columns = ["Conjunto", "n", "Média", "Mediana", "Moda", "Freq."]
    print("\nPreços de venda — bronze:")
    print(pd.DataFrame([row("Todos os registros", raw["valor_venda"])], columns=columns).to_string(index=False))
    groups = [
        row(label, silver.loc[silver["grupo"].eq(group), "valor_venda"])
        for group, label in GROUP_LABELS.items()
    ]
    print("\nPreços de venda — por grupo:")
    print(pd.DataFrame(groups, columns=columns).to_string(index=False))
