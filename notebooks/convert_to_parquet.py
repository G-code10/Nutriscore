import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"
OUTPUT_PATH = PROJECT_ROOT / "data" / "perimeter_partitioned"
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
from src.cleaning import prepare_data

NUTRIENTS = [
    "energy-kcal_100g",
    "fat_100g",
    "saturated-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
]
def parquet(df:pd.DataFrame, output_path) : 

    df["nutriscore_grade"] = df["nutriscore_grade"].astype('category')
    df["food_group"] = df["food_group"].astype('category')
    df[NUTRIENTS] = df[NUTRIENTS].astype('float32')

    shutil.rmtree(output_path, ignore_errors=True)
    df.to_parquet(output_path, partition_cols=['food_group'], index=False)

    return len(df)

def main():
    
    df = prepare_data(pd.read_parquet(PERIMETER_PATH))
    parquet(df, OUTPUT_PATH)

if __name__ == "__main__" :
    main()