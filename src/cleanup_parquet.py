import os, sys
sys.path.append(".")

import time
import re

import pandas as pd
import numpy as np

import conf

def extract_nutriment(liste_nutriments, nom_nutriment):
    if not isinstance(liste_nutriments, (np.ndarray, list)):
        return None

    for nutriment in liste_nutriments:
        if isinstance(nutriment, dict) and nutriment.get('name') == nom_nutriment:

            value_100g = nutriment.get('100g')
            try:
                value_100g = float(value_100g)
            except (TypeError, ValueError):
                return None

            if nom_nutriment == "fruits-vegetables-legumes-estimate-from-ingredients":
                return value_100g

            unit = nutriment.get('unit')
            if unit == "&#181;g":
                unit = 'µg'
            elif unit == "% vol / *":
                unit = '% vol'
            elif unit == "kJ":
                unit = 'kj'
            elif unit == "":
                unit = None

            if unit == "g":
                return value_100g
            elif unit == "mg":
                return value_100g * 0.001
            elif unit == "µg":
                return value_100g * 0.000001
            elif unit == "kj":
                return value_100g

            return None

    return None

def check_format(code):
    # 1. Vérification du format (strictement 8 ou 13 chiffres)
    if not re.match(r"^(\d{8}|\d{13})$", code):
        return None
        
    # 2. Vérification de la clé de contrôle (somme de contrôle GS1)
    chiffres = [int(x) for x in code]
    cle_reelle = chiffres[-1]      # Le dernier chiffre est la clé
    corps_du_code = chiffres[:-1]   # On isole le reste du code
    
    # En partant de la droite vers la gauche, les coefficients alternent toujours (3, 1, 3, 1...)
    total = sum(num * (3 if i % 2 == 0 else 1) for i, num in enumerate(reversed(corps_du_code)))
    
    cle_calculee = (10 - (total % 10)) % 10
    
    if cle_calculee != cle_reelle:
        return None
    
    return code

if not os.path.exists(conf.off_parquet_path_light):
    print(f"Le fichier parquet allégé n'est pas présent... Veuillez lancer generate_light_parquet.py pour le généré")
    exit()

start = time.time()
off_nutriments_tags_df = pd.read_parquet(conf.off_parquet_path_light)
print(f"Temps de chargement du fichier parquet allégé: {time.time() - start}")

start = time.time()
off_light_extended_df_fr = off_nutriments_tags_df.copy()
for name in conf.nutriments_list:
    print(f"Génération des données pour: {name}")
    off_light_extended_df_fr[name] = off_light_extended_df_fr['nutriments'].apply(lambda x: extract_nutriment(x, name))
print(f"Temps de génération des données: {time.time() - start}")

start = time.time()
off_light_extended_df_fr["short_name"] = off_light_extended_df_fr["product_name"].apply(lambda x: x[0]["text"] if isinstance(x, (list, np.ndarray)) and len(x) > 0 else None)
print(f"Temps de génération du nom court: {time.time() - start}")

start = time.time()
off_light_extended_df_fr["code_safe"] = 0
off_light_extended_df_fr["code_safe"] = off_light_extended_df_fr["code"].apply(lambda x: check_format(x))
off_light_extended_df_fr = off_light_extended_df_fr[~off_light_extended_df_fr["code_safe"].isna()].copy()

off_light_extended_df_fr.drop(columns=['nutriments'], inplace=True)
off_light_extended_df_fr.drop(columns=['product_name'], inplace=True)
off_light_extended_df_fr.drop(columns=['code_safe'], inplace=True)

off_light_extended_df_fr["brands"] = (off_light_extended_df_fr["brands"].replace("", pd.NA).fillna("Inconnu"))
off_light_extended_df_fr["brands"] = off_light_extended_df_fr["brands"].astype(str).str.replace("\x00", "", regex=False)

off_light_extended_df_fr["short_name"] = (off_light_extended_df_fr["short_name"].replace("", pd.NA).fillna("Inconnu"))

off_light_extended_df_fr["code"] = pd.to_numeric(off_light_extended_df_fr["code"], errors="coerce").astype("Int64")
off_light_extended_df_fr = off_light_extended_df_fr[off_light_extended_df_fr["code"].notna() & (off_light_extended_df_fr["code"] != 0)]
off_light_extended_df_fr.drop_duplicates(subset=["code"], inplace=True)

for col in ["short_name", "brands"]:
    off_light_extended_df_fr[col] = (
        off_light_extended_df_fr[col]
        .astype("string")
        .str.replace("\x00", "", regex=False)
    )
print(f"Netoyage divers: {time.time() - start}")

start = time.time()
off_light_extended_df_fr.to_parquet(conf.off_parquet_path_formated, index=False)
print(f"Temps de sauvegarde du fichier parquet formaté: {time.time() - start}")
