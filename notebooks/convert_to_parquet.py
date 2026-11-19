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

print("-- Préparation du parquet --")
df = prepare_data(pd.read_parquet(PERIMETER_PATH))

# category au lieu de str : équivalent de notre table "categories" en SQL permet de donner un id précis puisqu'il n'y a pas beaucoup de valeur différentes.
print("-- Modification des types --")
df["nutriscore_grade"] = df["nutriscore_grade"].astype('category')
df["food_group"] = df["food_group"].astype('category')
# float32 au lieu de float64 : nombre plus petit, moins précis, mais pèse moins en mémoire
df[NUTRIENTS] = df[NUTRIENTS].astype('float32')

print(f"-- Suppression du dossier : {OUTPUT_PATH} --")
# Placer ici pour éviter que si le départ du script ne fonctionne pas, qu'il évite de supprimer le dossier perimeter_partitioned
shutil.rmtree(OUTPUT_PATH, ignore_errors=True) # supprime le dossier et ce qu'il contient
print("-- Partition du parquet --")
df.to_parquet(OUTPUT_PATH, partition_cols=['food_group']) # partitionne par 'food_group' et créer donc 9 dossiers et 1 fichier dans chacun.

print(f"-- Partition effectuée dans {OUTPUT_PATH} --")