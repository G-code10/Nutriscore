import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"
CLEANING_PATH = PROJECT_ROOT / "data" / "clean" 
CLEANED_DATA_PATH = CLEANING_PATH / "cleaned_data.parquet"

from src.cleaning import prepare_data

def cleaning() : 
    df : pd.DataFrame = prepare_data(pd.read_parquet(PERIMETER_PATH))
    CLEANING_PATH.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CLEANED_DATA_PATH, index=False)
    return df

def main() :
    df = cleaning()
    return len(df)

if __name__ == "__main__":
    main()