import psycopg2
from psycopg2 import extras
import pandas as pd

def reset_database(cursor, sql_file_path):
    """Réinitialise la base de données (Idempotence)"""
    print("Réinitialisation de la base de données...")
    sql_file_path = '../../sql/postgre_creation.sql'
    with open(sql_file_path, 'r', encoding='utf-8') as file :
        sql_script = file.read()
        cursor.execute(sql_script)
    pass

def load_data():
    # 1. Paramètres de connexion
    conn = psycopg2.connect(
        dbname="nutriscope", 
        user="postgres", 
        password="postgres", 
        host="localhost"
    )
    cursor = conn.cursor()

    # 2. Idempotence : on recrée les tables
    reset_database(cursor, "../postgre_creation.sql")
    conn.commit()

    # 3. Lecture des données Pandas
    print("Chargement du fichier Parquet...")
    food_light_parquet = '../../data/food.parquet'
    df = pd.read_parquet(food_light_parquet)

    # 4. Préparation et insertion pour la table BRANDS
    print("Insertion des marques...")
    df_brands = (df['brands'][(df['brands'].notna() )&( df['brands'] != '')]
                .astype(str)
                .str.capitalize()
                .str.replace("\x00", "", regex=False) # Ici, regex=False fonctionne !
                .drop_duplicates())

    # - Rédige la requête INSERT appropriée
    tuples_brands = [(brand,)for brand in df_brands]
    query_brands = "INSERT INTO brands (name) VALUES %s ON CONFLICT (name) DO NOTHING"
    extras.execute_values(cursor, query_brands, tuples_brands)
    conn.commit() # SELECT COUNT(*) FROM brands : 416_271

    # 5. Préparation et insertion pour CATEGORIES
    print("Insertion des catégories...")

    df = df.drop_duplicates('code')

    df_copy = df.explode('categories_tags').copy()
    df_copy = df_copy[df_copy['categories_tags'].str.startswith('en:')].dropna()

    print(df_copy['categories_tags'].nunique()) # **:... 105_540 en:... 32_439

    df_categories = df_copy['categories_tags'].unique()

    print(df_categories)
    # TODO : CONTINUER ICI

    # 6. Préparation et insertion pour PRODUCTS
    print("Insertion des produits...")


    # 7. Préparation et insertion pour NUTRIMENTS
    print("Insertion des nutriments...")

    # Validation finale et fermeture
    conn.commit()
    cursor.close()
    conn.close()
    print("Chargement de la base NutriScope terminé avec succès !")

if __name__ == "__main__":
    load_data()