from dotenv import load_dotenv
from pathlib import Path

import pandas as pd

from src.api import get_all_items
from src.transform import transform_data as pd_transform
from src.charts import generate_charts
from src.report import print_audit, print_price_tables

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_FOLDER = BASE_DIR / "output"

RAW_DATA_FILE = OUTPUT_FOLDER / "bronze.csv"
DATA_FILE = OUTPUT_FOLDER / "silver.csv"

def get_raw_data():
    if RAW_DATA_FILE.exists():
        print(f"Fonte: cache ({RAW_DATA_FILE})")
        return

    print("Fonte: API da Sefaz-AL. Iniciando coleta...")

    response = get_all_items()
    response.to_csv(RAW_DATA_FILE)

    print(f"Bronze salvo: {RAW_DATA_FILE} ({len(response.produtos)} registros)")

def transform_data():
    df, audit = pd_transform(RAW_DATA_FILE, return_audit=True)
    df.to_csv(DATA_FILE, index=False)

    return df, audit

def main():
    get_raw_data()
    raw = pd.read_csv(RAW_DATA_FILE, dtype={"codigo": "string"})
    silver, audit = transform_data()

    print_audit(raw, audit)
    print_price_tables(raw, silver)
    print(f"\nSilver salvo: {DATA_FILE}")

    charts = generate_charts(DATA_FILE, OUTPUT_FOLDER / "charts")
    print(f"Gráficos gerados: {len(charts)}")

    for chart in charts:
        print(f"  {chart}")

    print("Processamento finalizado.")


if __name__ == "__main__":
    main()
