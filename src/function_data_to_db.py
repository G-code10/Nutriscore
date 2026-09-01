import pandas as pd
import sys

sys.path.append(".")

import nutriscore_sql
from conf import sql_conf_dict as conf

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

food_paquet = "data/food.parquet"

# Récupération et nettoyage des listes : 
df_products = pd.read_parquet(food_paquet, columns=["code", "brands", "product_name", "nutriments"]).head(5)
df_products.to_parquet("data/food_light.parquet")

# Puis je viens boucler sur mon tableau afin d'insérer la donnée en BDD
# for brand, _ in df_products.groupby("brands")["brands"]:
#     if brand != "":
#         NSQL.send_query("INSERT INTO marques (nom) VALUES (%s) ON CONFLICT (nom) DO NOTHING;", (str(brand),))

for code_col, brands_col, product_name_col, nutriments_col in df_products.itertuples(False, None):
    # Mes valeurs qui vont être à ajouter à la table produits
    code = code_col if len(code_col) == 13 else "Code error"
    marque_id = ""
    nom = ""
    lang = "main" # Par défaut "main"
    fiber = 0 # Par défaut 0
    proteins = 0 # Par défaut 0
    energy = 0 # Par défaut 0
    saturated_fat = 0 # Par défaut 0
    sugars = 0 # Par défaut 0
    salt = 0 # Par défaut 0
    
    # Boucle pour récupérer les nutriments :
    for nutriment_dict in nutriments_col:
        if nutriment_dict['name'] == 'fiber' :
            fiber = nutriment_dict['100g']
        elif nutriment_dict['name'] == 'proteins' :
            proteins = nutriment_dict['100g']
        elif nutriment_dict['name'] == 'energy' :
            energy = nutriment_dict['100g']
        elif nutriment_dict['name'] == 'saturated-fat' :
            saturated_fat = nutriment_dict['100g']
        elif nutriment_dict['name'] == 'sugars' :
            sugars = nutriment_dict['100g']
        elif nutriment_dict['name'] == 'salt' :
            salt = nutriment_dict['100g']

    NSQL.send_query("SELECT id FROM marques WHERE nom = %s", (brands_col,))
    for r in NSQL.fetch() : 
        marque_id = r[0]

    # df_products['product_name'][i] :
    # [
    #     {'lang': 'main', 'text': 'Véritable pâte à tartiner noisettes chocolat noir'},
    #     {'lang': 'fr', 'text': 'Véritable pâte à tartiner noisettes chocolat noir'}
    # ]

    # Boucle pour récupérer le nom et la lang
    for dictionnary in product_name_col:
        if dictionnary['lang'] != 'main' :
            lang = dictionnary['lang']
            nom = dictionnary['text']
        else : 
            nom = dictionnary['text']



    # Boucle pour récupérer la marque via requête, récupérer son id et l'insérer dans marque_id
    for brand in df_products['brands']:
        brand_query = "SELECT id, nom FROM marques WHERE "

    query = f"INSERT INTO produits (code, marque_id, nom, lang, fiber, proteins, energy, saturated-fat, sugars, salt) VALUES ('{code}','{marque_id}','{nom}','{lang}','{fiber}','{proteins}','{energy}','{saturated_fat}','{sugars}','{salt}')"

    NSQL.send_query(query=query)