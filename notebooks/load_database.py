"""
NutriScope - TP4 : chargement du périmètre dans PostgreSQL.

Rejouable : la base est détruite puis recréée à chaque lancement (sql/schemas.sql).
Tout est chargé en une seule transaction : en cas d'erreur, rien n'est enregistré.

Prérequis :
    - data/food_perimeter.parquet, produit par notebooks/build_perimeter.py ;
    - un PostgreSQL démarré avec une base "nutriscope" (conteneur Docker, port 5432).

Lancement, depuis la racine du projet :
    .venv\\Scripts\\python.exe notebooks\\load_database.py
"""

from getpass import getpass
from pathlib import Path

import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schemas.sql"

COLS = [
    "energy-kcal_100g",
    "fat_100g",
    "saturated-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
]

NUTRISCORE_GRADES = ["a", "b", "c", "d", "e"]

# Colonnes du parquet -> colonnes de la table nutriments
NUTRIMENTS_COLUMNS = {
    "code": "product_id",
    "energy-kcal_100g": "energy",
    "fat_100g": "fat",
    "saturated-fat_100g": "saturated_fat",
    "carbohydrates_100g": "carbohydrates",
    "sugars_100g": "sugars",
    "fiber_100g": "fiber",
    "proteins_100g": "proteins",
    "salt_100g": "salt",
}

NUTRIMENTS_SQL_COLS = [
    "product_id",
    "energy", "energy_u",
    "fat", "fat_u",
    "saturated_fat", "saturated_fat_u",
    "carbohydrates", "carbohydrates_u",
    "sugars", "sugars_u",
    "fiber", "fiber_u",
    "proteins", "proteins_u",
    "salt", "salt_u",
]


# ---------------------------------------------------------------------------
# Préparation des données (pandas)
# ---------------------------------------------------------------------------

def get_first_brand(brands):
    """Récupère la première marque d'un produit"""
    if not isinstance(brands, str):
        return None
    list_brands = [" ".join(brand.split()).lower() for brand in brands.split(",")]
    if list_brands[0] == "" or list_brands == []:
        return None
    return list_brands[0]


def prepare_data(df):
    """Doublons, marque, Nutri-Score, valeurs impossibles."""
    # Doublons de codes-barres : on trie du plus rempli au moins rempli,
    # drop_duplicates() garde la première ligne rencontrée, donc la plus complète.
    df["not_na_count"] = df.notna().sum(axis=1)
    df = df.sort_values("not_na_count", ascending=False).drop_duplicates("code")
    df = df.drop(columns=["not_na_count"])

    df["brand"] = df["brands"].apply(get_first_brand)

    # Liste blanche : plus sûre face à des valeurs inconnues.
    df["nutriscore_grade"] = df["nutriscore_grade"].where(df["nutriscore_grade"].isin(NUTRISCORE_GRADES))

    # Valeurs impossibles -> NaN (énergie : 0 à 950 kcal, le reste : 0 à 100 g)
    for col in COLS:
        if col == "energy-kcal_100g":
            mask = (df[col] < 0) | (df[col] > 950)
        else:
            mask = (df[col] < 0) | (df[col] > 100)
        df.loc[mask, col] = np.nan

    return df


def to_rows(df, columns):
    """Liste de tuples prête pour execute_values, avec None à la place de NaN."""
    selection = df[columns]
    selection = selection.astype(object).where(selection.notna(), None)
    return list(selection.itertuples(index=False, name=None))


# ---------------------------------------------------------------------------
# Chargement (PostgreSQL)
# ---------------------------------------------------------------------------

def reset_database(cursor):
    """Détruit et recrée les tables."""
    with open(SCHEMA_PATH, encoding="utf-8") as file:
        cursor.execute(file.read())


def insert_brands(cursor, df):
    brands = df["brand"].dropna().unique()
    brands = [(brand,) for brand in brands]
    execute_values(cursor, "INSERT INTO brands (name) VALUES %s ON CONFLICT (name) DO NOTHING", brands)

    cursor.execute("SELECT name, id FROM brands")
    return dict(cursor.fetchall())


def insert_categories(cursor, df):
    food_groups = df["food_group"].unique()
    food_groups = [(food_group, True) for food_group in food_groups]

    categories_tags = df["categories_tags"].explode()
    categories_tags = categories_tags.dropna().unique()
    categories_tags = [(categorie_tag, False) for categorie_tag in categories_tags]

    # Ici l'ordre est important : food_groups possède des rayons identiques à des catégories.
    # Pour garder (name, True), food_groups doit être ajouté en premier,
    # autrement (name, False) prendrait le dessus.
    execute_values(cursor, "INSERT INTO categories (name, main) VALUES %s ON CONFLICT (name) DO NOTHING", food_groups)
    execute_values(cursor, "INSERT INTO categories (name, main) VALUES %s ON CONFLICT (name) DO NOTHING", categories_tags)

    cursor.execute("SELECT name, id FROM categories")
    return dict(cursor.fetchall())


def insert_products(cursor, df, brands_id):
    df = df.assign(brand_id=df["brand"].map(brands_id))
    rows = to_rows(df, ["code", "brand_id", "brand", "product_name", "nutriscore_grade"])
    execute_values(
        cursor,
        "INSERT INTO products (code, brand_id, brand, name, nutriscore_grade) VALUES %s",
        rows,
        page_size=10_000,
    )
    return len(rows)


def insert_products_categories(cursor, df, categories_ids):
    categories = df[["code", "categories_tags"]].explode("categories_tags")
    categories = categories.rename(columns={"categories_tags": "category"})

    food_group = df[["code", "food_group"]].rename(columns={"food_group": "category"})

    # Un produit ne doit avoir qu'un seul rayon : on retire des catégories
    # ordinaires celles qui portent un nom de rayon.
    food_group_names = df["food_group"].unique()
    categories = categories[~categories["category"].isin(food_group_names)]

    cat_concat = pd.concat([food_group, categories]).drop_duplicates()
    cat_concat["category_id"] = cat_concat["category"].map(categories_ids)

    rows = to_rows(cat_concat, ["category_id", "code"])
    execute_values(
        cursor,
        "INSERT INTO products_categories (category_id, product_id) VALUES %s",
        rows,
        page_size=10_000,
    )
    return len(rows)


def insert_nutriments(cursor, df):
    nutriments = df[list(NUTRIMENTS_COLUMNS)].rename(columns=NUTRIMENTS_COLUMNS)
    nutriments["energy_u"] = "kcal"
    nutriments[["fat_u", "saturated_fat_u", "carbohydrates_u", "sugars_u", "fiber_u", "proteins_u", "salt_u"]] = "g"

    rows = to_rows(nutriments, NUTRIMENTS_SQL_COLS)
    query = f"INSERT INTO nutriments ({', '.join(NUTRIMENTS_SQL_COLS)}) VALUES %s"
    execute_values(cursor, query, rows, page_size=10_000)
    return len(rows)


def main():
    print(f"Lecture de {PERIMETER_PATH}...")
    df = prepare_data(pd.read_parquet(PERIMETER_PATH))
    print(f"{len(df):,} produits à charger")

    conn = psycopg2.connect(
        dbname="nutriscope",
        host="localhost",
        port="5432",
        user="postgres",
        password=getpass("Mot de passe : "),
    )
    try:
        with conn.cursor() as cursor:
            print("Réinitialisation de la base...")
            reset_database(cursor)

            # Ordre imposé par les clés étrangères : on insère d'abord ce vers quoi on pointe.
            brands_id = insert_brands(cursor, df)
            print(f"brands : {len(brands_id):,}")

            categories_ids = insert_categories(cursor, df)
            print(f"categories : {len(categories_ids):,}")

            print(f"products : {insert_products(cursor, df, brands_id):,}")
            print(f"products_categories : {insert_products_categories(cursor, df, categories_ids):,}")
            print(f"nutriments : {insert_nutriments(cursor, df):,}")

        conn.commit()
        print("Chargement terminé.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
