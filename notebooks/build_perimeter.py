from pathlib import Path

import numpy as np
import pandas as pd

# Racine du projet : le dossier parent de notebooks/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "food.parquet"
PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"

COLUMNS = [
    "code",
    "product_name",
    "brands",
    "categories_tags",
    "food_groups_tags",
    "countries_tags",
    "nutriscore_grade",
    "nutriments",
]

NUTRIENTS = [
    "energy-kcal",
    "fat",
    "saturated-fat",
    "carbohydrates",
    "sugars",
    "fiber",
    "proteins",
    "salt",
]

NUTRIENT_COLS = [name + "_100g" for name in NUTRIENTS]

FOOD_GROUPS = [
    "en:sugary-snacks",
    "en:fish-meat-eggs",
    "en:cereals-and-potatoes",
    "en:milk-and-dairy-products",
    "en:beverages",
    "en:fats-and-sauces",
    "en:fruits-and-vegetables",
    "en:composite-foods",
    "en:salty-snacks",
]

NUTRISCORE_GRADES = ["a", "b", "c", "d", "e"]


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def get_100g(nutrients, name):
    """Renvoie la valeur pour 100 g du nutriment `name`, ou NaN s'il est absent."""
    if nutrients is None:
        return np.nan
    for nutrient in nutrients:
        if nutrient["name"] == name:
            return nutrient["100g"]
    return np.nan


def get_name(names):
    """Renvoie le nom en français, sinon le nom principal, sinon NaN."""
    if names is None:
        return np.nan
    main_name = np.nan
    for name in names:
        if name["lang"] == "fr":
            return name["text"]
        if name["lang"] == "main":
            main_name = name["text"]
    return main_name


def get_food_group(groups):
    """Renvoie le groupe alimentaire de niveau 1 (le rayon), ou NaN."""
    if groups is None or len(groups) == 0:
        return np.nan
    return groups[0]


def load_france(path):
    """Charge les produits vendus en France, avec des colonnes simples (aplaties)."""
    df = pd.read_parquet(path, columns=COLUMNS)
    is_france = df["countries_tags"].apply(lambda tags: tags is not None and "en:france" in tags)
    df_fr = df[is_france].copy()
    del df

    for name in NUTRIENTS:
        df_fr[name + "_100g"] = df_fr["nutriments"].apply(lambda nutrients: get_100g(nutrients, name))
    df_fr["product_name"] = df_fr["product_name"].apply(get_name)
    df_fr["food_group"] = df_fr["food_groups_tags"].apply(get_food_group)

    return df_fr.drop(columns=["nutriments", "countries_tags", "food_groups_tags"])


# ---------------------------------------------------------------------------
# Rapports
# ---------------------------------------------------------------------------

def print_tp1_report(df):
    """Affiche les réponses aux cinq questions du TP1."""
    print("\n=== TP1 ===")
    print(f"Q1 - Produits vendus en France : {len(df):,}")

    graded = df["nutriscore_grade"].isin(NUTRISCORE_GRADES).mean() * 100
    print(f"Q2 - Nutri-Score de A à E : {graded:.1f} %")

    brands = (
        df["brands"]
        .replace("", np.nan)
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .str.lower()
    )
    print("Q3 - Top 10 marques :")
    print(brands.value_counts().head(10).to_string())

    print("Q4 - Manquants sur les nutriments clés :")
    for col in ["energy-kcal_100g", "sugars_100g", "salt_100g"]:
        print(f"    {col} : {df[col].isna().mean() * 100:.1f} %")


def print_profiling_report(df):
    """Affiche les principaux problèmes de qualité relevés au TP2."""
    print("\n=== TP2 - Profiling ===")
    duplicated = df["code"].duplicated(keep=False)
    print(f"Lignes avec un code-barres en double : {duplicated.sum()}")

    over_100 = (df[NUTRIENT_COLS].drop(columns="energy-kcal_100g") > 100).any(axis=1)
    print(f"Produits avec un nutriment > 100 g/100 g : {over_100.sum()}")

    negative = (df[NUTRIENT_COLS] < 0).any(axis=1)
    print(f"Produits avec une valeur négative : {negative.sum()}")

    print(f"Produits > 900 kcal/100 g : {(df['energy-kcal_100g'] > 900).sum()}")
    print(f"Produits à 0 kcal/100 g : {(df['energy-kcal_100g'] == 0).sum()}")

    no_category = df["categories_tags"].apply(lambda tags: tags is None or len(tags) == 0)
    print(f"Produits sans catégorie : {no_category.sum():,} ({no_category.mean() * 100:.1f} %)")
    print(f"Produits sans rayon : {df['food_group'].isna().sum():,} ({df['food_group'].isna().mean() * 100:.1f} %)")


# ---------------------------------------------------------------------------
# Périmètre
# ---------------------------------------------------------------------------

def filter_perimeter(df):
    """Garde les produits des rayons retenus qui ont un code, un nom et une énergie."""
    in_groups = df["food_group"].isin(FOOD_GROUPS)
    is_complete = (
        df["code"].notna()
        & df["product_name"].notna()
        & df["energy-kcal_100g"].notna()
    )
    return df[in_groups & is_complete].copy()


def main():
    print(f"Chargement de {RAW_PATH} (environ 3 minutes)...")
    df_fr = load_france(RAW_PATH)

    print_tp1_report(df_fr)
    print_profiling_report(df_fr)

    df_perimeter = filter_perimeter(df_fr)
    print("\n=== TP2 - Périmètre ===")
    print(f"Produits retenus : {len(df_perimeter):,}")
    print(df_perimeter["food_group"].value_counts().to_string())

    df_perimeter.to_parquet(PERIMETER_PATH, index=False)
    print(f"\nPérimètre sauvegardé dans {PERIMETER_PATH}")


if __name__ == "__main__":
    main()