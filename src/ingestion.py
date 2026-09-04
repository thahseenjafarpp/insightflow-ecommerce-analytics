from pathlib import Path
import pandas as pd


RAW_DATA_PATH = Path("data/raw")


def load_csv(file_name):
    """
    Load a CSV file from the raw data directory.
    """
    file_path = RAW_DATA_PATH / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def load_all_data():
    """
    Load all Olist CSV files into a dictionary of DataFrames.
    """
    data = {}

    for file_path in RAW_DATA_PATH.glob("*.csv"):
        data[file_path.stem] = pd.read_csv(file_path)

    return data