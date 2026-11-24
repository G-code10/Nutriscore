import pandas as pd
import sys
import hashlib
import json

from pathlib import Path
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"
FEATURES_PATH = PROJECT_ROOT / "data" / "features.parquet"

from src.cleaning import prepare_data
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
SEED = 42
TEST_SIZE = 0.2

def export_features(df, export_to, force=False):
    """Retire les lignes où le nutriscore_grade vide et garde les lignes cohérentes. Puis étale food_group, cela ajoute donc 9 colonnes. Pour finir changer le type du NS_g en category et float32 pour les nutriments afin de réduire l'espace en mémoire, ainsi fluidifié le chargement.
    Création d'une colonne split 80/20 "train"/"test" par le biais de train_test_split().
    """
    if export_to.exists() and not force :
        raise FileExistsError(f"{export_to} existe déjà. Relancer avec --force pour écraser le fichier.")
    
    df = df[df['nutriscore_grade'].notna() & ~df['is_incoherent']]
    df = df[COLS]
    df = pd.get_dummies(df, columns=[FEATURE])

    df["nutriscore_grade"] = df["nutriscore_grade"].astype('category')
    df[NUTRIENTS] = df[NUTRIENTS].astype('float32')

    df['split'] = "train" # par défaut, remplir la colonne par "train"
    df = df.sort_values("code").reset_index(drop=True)
    train_idx, test_idx = train_test_split(
        df.index,
        test_size=TEST_SIZE,
        stratify= df['nutriscore_grade'],
        random_state=SEED, # la graine par défaut, permet garder le même tirage.
    )
    df.loc[test_idx, "split"] = "test"
    df.to_parquet(export_to, index=False)
    export_json(df, export_to)
    return len(df)

def export_json(df : pd.DataFrame, export_to:Path):
    """Créer un schéma .json avec :
    - nom du fichier
    - lignes
    - les informations du split
    - filtres
    - sha256
    - les règles d'usage
    - source"""
    content = export_to.read_bytes()
    fingerprint = hashlib.sha256(content).hexdigest()
    counts = pd.crosstab(df['nutriscore_grade'], df['split']).to_dict()
    schema = {
        "fichier" : export_to.name,
        "lignes" : len(df),
        "split" : {
            "methode" : "train_test_split stratifié sur nutriscore_grade",
            "graine" : SEED,
            "part_test" : TEST_SIZE,
            "effectifs" : counts,
        },
        "filtres" : [
            "nutriscore_grade non vide",
            "is_incoherent à False"
        ],
        "sha256" : fingerprint,
        "regle_usage" : "fit sur le train seulement; le test n'est regardé qu'une fois, à la fin; la validation croisée se fait à l'intérieur du train.",
        "source" : "Open Food Facts contributors, licence ODbL"
    }

    schema_path = export_to.parent / "schema.json"

    with open(schema_path, "w", encoding="utf-8") as file :
        json.dump(schema, file, indent=4, ensure_ascii=False)
    return True

def main():
    
    df = prepare_data(pd.read_parquet(PERIMETER_PATH))
    export_features(df, FEATURES_PATH)


if __name__ == "__main__" :
    main()