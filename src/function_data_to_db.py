import pandas as pd
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
# df_products.to_parquet("data/food_light.parquet")


print("Récupération des marques, envoie en base de donnée les marques ...")
# Puis je viens boucler sur mon tableau afin d'insérer la donnée en BDD
for brand, _ in df_products.groupby("brands")["brands"]:
    if brand != "":
        NSQL.send_query("INSERT INTO marques (nom) VALUES (%s) ON CONFLICT (nom) DO NOTHING;", (str(brand),))

print("Insertion sur la table Produits")
for code_col, brands_col, product_name_col, nutriments_col in df_products.itertuples(False, None):
    # Mes valeurs qui vont être à ajouter à la table produits
    while len(code_col) < 13 :
        code_col = "0" + code_col
    code = code_col
    marque_id = ""
    name = ""
    lang = ""
    fiber = 0 # Par défaut 0
    proteins = 0 # Par défaut 0
    energy = 0 # Par défaut 0
    saturated_fat = 0 # Par défaut 0
    sugars = 0 # Par défaut 0
    salt = 0 # Par défaut 0
    
    print("Nutriments")
    ############# NUTRIMENTS #############
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

    print("Marques ID")
    ############# MARQUE_ID #############
    NSQL.send_query("SELECT id FROM marques WHERE nom = %s", (brands_col,))
    for r in NSQL.fetch() : 
        marque_id = r[0]

    # df_products['product_name'][i] :
    # [
    #     {'lang': 'main', 'text': 'Véritable pâte à tartiner noisettes chocolat noir'},
    #     {'lang': 'fr', 'text': 'Véritable pâte à tartiner noisettes chocolat noir'}
    # ]

    print("Nom & langue")
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

    print(f"Finalisation, envoie de toutes les données")
    NSQL.send_query("INSERT INTO produits (code, marque_id, nom, lang, fiber, proteins, energy, saturated-fat, sugars, salt) VALUES (%s);",(code, marque_id, name, lang,fiber, proteins,energy,saturated_fat,sugars,salt))
    print(f"On recommence")