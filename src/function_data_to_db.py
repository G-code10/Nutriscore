import pandas as pd
import numpy as np
import math
import sys

sys.path.append(".")

import nutriscore_sql
from conf import sql_conf_dict as conf
print("Import effectué")

conf = {
    "database": "nutriscope", 
    "user": "postgres", 
    "host": "localhost", 
    "port": 5432,
    "debug": False
}

NSQL = nutriscore_sql.NutriscoreSQL(conf, "postgres")

# TODO : 
# Créer des fonctions, des boucles afin de pouvoir récupérer et insérer les données en BDD

food_paquet = "data/food_light.parquet"

print("Récupération du parquet")
# Récupération et nettoyage des listes : 
df_products = pd.read_parquet(food_paquet, columns=["code", "brands", "product_name", "nutriments"])
# # df_products.to_parquet("data/food_light.parquet")
print(f"Parquet récupéré : {food_paquet}")

# print(df_products[df_products['brands'].isna() | df_products['brands'] == ""])



print("Récupération des marques, envoie en base de donnée les marques ...")
# Puis je viens boucler sur mon tableau afin d'insérer la donnée en BDD
NSQL.send_query("INSERT INTO marques (nom) VALUES ('Unknown') ON CONFLICT (nom) DO NOTHING;")
for brand, _ in df_products.groupby("brands")["brands"]:
    if brand != "" and brand.lower() != 'nan':
        NSQL.send_query("INSERT INTO marques (nom) VALUES (%s) ON CONFLICT (nom) DO NOTHING;", (str(brand),))
print("Table marques remplie")
 
def look_for_unit(nutri_dict):
    unit = nutri_dict.get('unit', 'g')
    if unit == "&#181;g":
        unit = 'µg'
    elif unit == "% vol / *":
        unit = '% vol'
    elif unit == "kJ":
        unit = 'kj'
    elif unit == "":
        unit = 2.1
    return unit 

def change_data_from_unit(unit, nutri_value):
    """"! Permet de modifier la valeur (nutri_value) selon son unité de mesure"""
    if unit == "g":
        return float(nutri_value)
    elif unit == "mg":
        return float(nutri_value * 0.001)
    elif unit == "µg":
        return float(nutri_value * 0.000001)
    elif unit == "kj":
        return float(nutri_value)
    else:
        return 0.0
    
print("Insertion sur la table Produits")
loop_count = 0
for code_col, brands_col, product_name_col, nutriments_col in df_products.itertuples(False, None):
    # Vérifier si les infos existent
    if not isinstance(nutriments_col, (np.ndarray, list)) :
        continue
    # Mes valeurs qui vont être à ajouter à la table produits
    
    code = int(code_col)
    marque_id = ""
    name = ""
    lang = ""
    fiber = 0.0 # Par défaut 0.0
    proteins = 0.0 # Par défaut 0.0
    energy = 0.0 # Par défaut 0.0
    saturated_fat = 0.0 # Par défaut 0.0
    sugars = 0.0 # Par défaut 0.0
    salt = 0.0 # Par défaut 0.0

    ############# NUTRIMENTS #############
    # Boucle pour récupérer les nutriments :
    
    for nutriment_dict in nutriments_col:

        if nutriment_dict['name'] == 'fiber' :
            try:
                unit = look_for_unit(nutriment_dict)
                fiber = change_data_from_unit(unit, nutriment_dict['100g'])
            except (TypeError,ValueError):
                fiber = 0.0

        elif nutriment_dict['name'] == 'proteins' :
            try:
                unit = look_for_unit(nutriment_dict)
                proteins = change_data_from_unit(unit, nutriment_dict['100g'])
            except (TypeError,ValueError):
                proteins = 0.0

        elif nutriment_dict['name'] == 'energy' :
            try:
                unit = look_for_unit(nutriment_dict)
                energy = change_data_from_unit(unit, nutriment_dict['100g'])
            except (TypeError,ValueError):
                energy = 0.0

        elif nutriment_dict['name'] == 'saturated-fat' :
            try:
                unit = look_for_unit(nutriment_dict)
                saturated_fat = change_data_from_unit(unit, nutriment_dict['100g'])
            except (TypeError,ValueError):
                saturated_fat = 0.0

        elif nutriment_dict['name'] == 'sugars' :
            try:
                unit = look_for_unit(nutriment_dict)
                sugars = change_data_from_unit(unit, nutriment_dict['100g'])
            except (TypeError,ValueError):
                sugars = 0.0

        elif nutriment_dict['name'] == 'salt' :
            try:
                unit = look_for_unit(nutriment_dict)
                salt = change_data_from_unit(unit, nutriment_dict['100g'])
            except (TypeError,ValueError):
                salt = 0.0

    ############# MARQUE_ID #############
    if str(brands_col).lower() == "nan" or brands_col == "":
        continue
    else : 
        NSQL.send_query("SELECT id FROM marques WHERE nom = %s", (brands_col,))
        for r in NSQL.fetch() : 
            marque_id = r[0]

    ############# NOM & LANG #############
    # Boucle pour récupérer le nom et la lang
    for product_name_dict in product_name_col:
        if product_name_dict['lang'] != 'main' :
            lang = product_name_dict['lang']
            name = product_name_dict['text']
            break
        else : 
            lang = "main"
            name = product_name_dict['text']

    NSQL.send_query("INSERT INTO produits (code, marque_id, nom, lang, fiber, proteins, energy, saturated_fat, sugars, salt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (code) DO NOTHING;",(code, marque_id, name, lang,fiber, proteins,energy,saturated_fat,sugars,salt,))

    loop_count += 1

print("Tables remplies")
print(f'Nombre de requêtes : {loop_count} / {len(df_products['code'])}')