import pandas as pd
# import nutriscore_sql
# import math
import sys

sys.path.append(".")

from cleaning import (flatten_nutriments, flattening_column_join_and_drop)
from conf import sql_conf_dict as conf
print("Import effectué")

conf = {
    "database": "nutriscope", 
    "user": "postgres", 
    "host": "localhost", 
    "port": 5432,
    "debug": False
}

# NSQL = nutriscore_sql.NutriscoreSQL(conf, "postgres")

# TODO : 
# Créer des fonctions, des boucles afin de pouvoir récupérer et insérer les données en BDD
def print_df(df:pd.DataFrame, nbr_of_line:int, column:list = []) :
    if column != [] :
        if nbr_of_line != '':
            print(df[column].head(nbr_of_line))
        else :
            print(df[column])
    else :
        if nbr_of_line != '':
            print(df.head(nbr_of_line))
        else :
            print(df)

paquet_choice = True
food_paquet = ''

# Nettoyer la donnée et créer un fichier .parquet
while paquet_choice :

    choose_paquet = input("Initialiser un paquet en cleaned - light(l) ou regular(r)\nOU next(n) pour passer à la suite : ")

    if choose_paquet == 'light' or choose_paquet == 'l' :
        food_paquet = "data/food_light.parquet"
    elif choose_paquet == 'regular' or choose_paquet == 'r' :
        food_paquet = "data/food.parquet"
    else :
        paquet_choice = False
        break

    print("Récupération du parquet")
    # Récupération et nettoyage des listes : 
    df_products = pd.read_parquet(food_paquet, columns=["code", "brands", "product_name", "nutriments"])#.head(10_000) ==> light_food
    # df_products.to_parquet("data/food_light.parquet")
    print(f"Parquet récupéré : {food_paquet}")

    print('Création de ma colonne flat_nutriments')
    df_products['flat_nutriments'] = df_products['nutriments'].apply(lambda x : flatten_nutriments(x))
    print('Colonne flat_nutriments finie')

    print('Étaler flat_nutriments et suppression de celle-ci et de nutriments')
    df_join = flattening_column_join_and_drop(df_products['flat_nutriments'], df_products, ['nutriments', 'flat_nutriments'])
    print('Jointure et suppression finie')

    print('Exportation en parquet')
    if food_paquet == "data/food_light.parquet" :
        df_join.to_parquet("data/cleaned_food_light.parquet")
    elif food_paquet == "data/food.parquet" :
        df_join.to_parquet("data/cleaned_food.parquet")
    print('Exportation finie')

    paquet_choice = False

# Manipulation de la donnée
data_choice = True
while data_choice:

    choose_paquet = input("Choisissez un parquet nettoyé : light(l) ou regular(r)\nOU quit(q) pour quitter : ")

    if choose_paquet == 'light' or choose_paquet == 'l' :
        food_paquet = "data/cleaned_food_light.parquet" 
    elif choose_paquet == 'regular' or choose_paquet == 'r' :
        food_paquet = "data/cleaned_food.parquet" 
    else :
        data_choice = False
        break

    # Charger le parquet 
    df_products = pd.read_parquet(food_paquet)
    print(f"Voici les colonnes du {food_paquet} :\n{df_products.columns}")

    while data_choice :

        columns_input = []
        columns_continue = True

        while columns_continue : 
            display_df = input("Quelles colonnes voulez-vous afficher ?\nq - Quitter (dernier tour) : ")
            if display_df.lower() in df_products.columns :
                columns_input.append(display_df.lower())
            elif display_df.lower() == 'q' or display_df.lower() == 'quitter':
                columns_continue = False
                data_choice = False
            else : 
                print("Vérifiez que la colonne existe...")
                continue

        nbr_of_line = -131197 
        while nbr_of_line < 0 :
            try :
                nbr_of_line = int(input(f'Combien de lignes afficher ? (0 - {len(df_products)})\nEntrez "0" si vous ne voulez rien mettre : '))
            except :
                continue    
            if nbr_of_line > 0 :
                print_df(df_products,nbr_of_line, columns_input)
            else : 
                data_choice = False