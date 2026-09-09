import os, sys
sys.path.append(".")

import io
import time

import csv

import pandas as pd
import numpy as np

import nutriscore_sql
import conf

if not os.path.exists(conf.off_parquet_path_formated):
    print(f"Le fichier parquet formaté n'est pas présent... Veuillez lancer cleanup_parquet.py pour le généré")
    exit()

start = time.time()
off_nutriments_tags_df = pd.read_parquet(conf.off_parquet_path_formated)
print(f"Temps de chargement du fichier parquet formaté: {time.time() - start}")

NSQL = nutriscore_sql.NutriscoreSQL(conf.sql_conf_dict, "simirblaiti")

sql_db_struct = "../sql/postgre_creation.sql"
NSQL.send_file(sql_db_struct)

brands = off_nutriments_tags_df["brands"].dropna().unique()
values = [(brand,) for brand in brands]

off_nutriments_tags_df["brand"] = off_nutriments_tags_df["brands"] # pour traitement avant finalisation
off_nutriments_tags_df["brands"] = 1 # marque_id à 1 pour le moment
off_nutriments_tags_df["lang"] = "fr"

start = time.time()
NSQL.add_values(conf.add_brand_query_ex, values, );
print(f"Insertion des marques: {time.time() - start}")

buffer = io.StringIO()

df_copy = off_nutriments_tags_df[[
    "code",
    "brands",
    "brand",
    "short_name",
    "lang", 
    "fiber",
    "proteins",
    "energy",
    "saturated-fat",
    "sugars",
    "salt"
]].copy()

start = time.time()
df_copy.to_csv(buffer, sep="\t", header=False, index=False, na_rep="\\N")
print(f"Création du CSV en mémoire: {time.time() - start}")

buffer.seek(0)

start = time.time()
NSQL.copy_products(conf.copy_product, buffer)
print(f"Insertion des produits: {time.time() - start}")

start = time.time()
NSQL.send_query(conf.update_marque_id_query)
print(f"Création des liaisons produit/marque: {time.time() - start}")

NSQL.send_query(conf.finalize_table)
