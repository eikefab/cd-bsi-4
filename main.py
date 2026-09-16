from dotenv import load_dotenv
from os import path
from pathlib import Path

from src.api import get_all_items
from src.transform import transform_data as pd_transform
from src.charts import generate_charts

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

OUTPUT_FOLDER = BASE_DIR / "output"

RAW_DATA_FILE = OUTPUT_FOLDER / "bronze.csv"
DATA_FILE = OUTPUT_FOLDER / "silver.csv"

def get_raw_data():
    if path.exists(RAW_DATA_FILE):
        print(f"Raw data file {RAW_DATA_FILE} already exists. Skipping data retrieval.")

        return

    response = get_all_items()
    response.to_csv(RAW_DATA_FILE)

def transform_data():
    df = pd_transform(RAW_DATA_FILE)
    df.to_csv(DATA_FILE, index=False)

def main():
    get_raw_data()
    transform_data()
    generate_charts(DATA_FILE, OUTPUT_FOLDER / "charts")


if __name__ == "__main__":
    main()
