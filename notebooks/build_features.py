import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"
FEATURES_PATH = PROJECT_ROOT / "data" / "features.parquet"

from src.cleaning import prepare_data

print(f"-- Récupération du {PERIMETER_PATH} --")
print("-"*50)
df = prepare_data(pd.read_parquet(PERIMETER_PATH))
print(f"Récupération effectuée...")
print("-"*50)

COLS = [
    'code',
    'product_name',
    'nutriscore_grade',
    'energy-kcal_100g', 
    'fat_100g', 
    'saturated-fat_100g',
    'carbohydrates_100g', 
    'sugars_100g', 
    'fiber_100g', 
    'proteins_100g',
    'salt_100g', 
    'food_group'
]

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

FEATURE = "food_group"

print(f"-- Nettoyage en cours --")
print("-"*50)

print(f"Retirer NutriScore manquant et les valeurs incohérentes")
before = len(df)
df = df[df['nutriscore_grade'].notna() & ~df['is_incoherent']]
after = len(df)
print(f"{before - after} lignes retirées")

print(f"Colonnes gardées : {COLS}")
df = df[COLS]

print(f"Étalement de la colonne '{FEATURE}'")
df = pd.get_dummies(df, columns=[FEATURE])

print("Changements de type pour les colonnes")
df["nutriscore_grade"] = df["nutriscore_grade"].astype('category')
df[NUTRIENTS] = df[NUTRIENTS].astype('float32')

print("-"*50)
print(f"Export en .parquet vers {FEATURES_PATH}")
df.to_parquet(FEATURES_PATH, index=False)
print("Export effectué...")

print("-"*50)
print("Test de récupération du features.parquet")
df = pd.read_parquet(FEATURES_PATH)
print(f"Nombre de lignes : {len(df)}")
print(f"Nombre de colonnes : {df.shape[1]}")
print(f"Colonnes : {list(df.columns)}")