# Introduction

Un nouveau périmètre a été défini après étude du cas et plusieurs essaies avec l'anciens périmètre (perimetre.md)

Effectué avec l'aide de : [Tablesgenerator](https://www.tablesgenerator.com/markdown_tables)

# Informations sur le parquet
 
Dans le format choisi (parquet) il y à un total de 111 colonnes pour 4636471 produits
 
Si dessous ce trouve la liste des colonnes et leurs infos
 
| Colonne | Type | % Remplissage | Mémoire (MB) |
| --- | --- | --- | --- |
| additives_n | int32 | 27.96 | 35.37 |
| additives_tags | object | 29.0 | 229.21 |
| allergens_tags | object | 99.07 | 526.66 |
| brands_tags | object | 65.61 | 384.61 |
| brands | str | 65.6 | 66.09 |
| categories | str | 40.06 | 171.23 |
| categories_tags | object | 43.59 | 291.17 |
| categories_properties | object | 99.06 | 842.01 |
| checkers_tags | object | 100.0 | 530.6 |
| ciqual_food_name_tags | object | 29.75 | 232.38 |
| cities_tags | object | 20.71 | 194.04 |
| code | str | 100.0 | 92.14 |
| compared_to_category | str | 38.54 | 63.32 |
| complete | int32 | 100.0 | 35.37 |
| completeness | float32 | 100.0 | 17.69 |
| correctors_tags | object | 100.0 | 530.6 |
| countries_tags | object | 99.79 | 529.71 |
| created_t | int64 | 100.0 | 35.37 |
| creator | str | 100.0 | 80.48 |
| data_quality_errors_tags | object | 99.07 | 526.66 |
| data_quality_info_tags | object | 99.07 | 526.66 |
| data_quality_warnings_tags | object | 99.2 | 527.22 |
| data_sources_tags | object | 86.8 | 474.58 |
| environmental_score_data | str | 82.11 | 9950.94 |
| environmental_score_grade | str | 82.11 | 56.74 |
| environmental_score_score | int32 | 19.28 | 35.37 |
| environmental_score_tags | object | 82.11 | 454.67 |
| editors | object | 1.24 | 111.4 |
| emb_codes_tags | object | 20.71 | 194.04 |
| emb_codes | str | 18.81 | 38.76 |
| entry_dates_tags | object | 100.0 | 530.6 |
| food_groups_tags | object | 99.06 | 526.63 |
| generic_name | object | 100.0 | 530.6 |
| images | object | 100.0 | 530.6 |
| informers_tags | object | 100.0 | 530.6 |
| ingredients_analysis_tags | object | 29.63 | 231.89 |
| ingredients_from_palm_oil_n | float64 | 19.94 | 35.37 |
| ingredients_n | int32 | 27.96 | 35.37 |
| ingredients_original_tags | object | 27.96 | 224.8 |
| ingredients_percent_analysis | float64 | 25.98 | 35.37 |
| ingredients_tags | object | 27.96 | 224.8 |
| ingredients_text | object | 100.0 | 530.6 |
| ingredients_with_specified_percent_n | int32 | 27.96 | 35.37 |
| ingredients_with_unspecified_percent_n | int32 | 27.96 | 35.37 |
| ingredients_without_ciqual_codes_n | int32 | 27.96 | 35.37 |
| ingredients_without_ciqual_codes | object | 27.96 | 224.79 |
| ingredients | str | 27.96 | 7910.68 |
| known_ingredients_n | int32 | 27.96 | 35.37 |
| labels_tags | object | 36.73 | 262.03 |
| labels | str | 33.27 | 73.68 |
| lang | str | 100.0 | 44.22 |
| languages_tags | object | 100.0 | 530.6 |
| last_edit_dates_tags | object | 100.0 | 530.6 |
| last_editor | str | 97.03 | 94.17 |
| last_image_t | int64 | 75.91 | 35.37 |
| last_modified_by | str | 96.96 | 94.09 |
| last_modified_t | int64 | 100.0 | 35.37 |
| last_updated_t | int64 | 100.0 | 35.37 |
| link | str | 18.97 | 40.08 |
| main_countries_tags | object | 100.0 | 530.6 |
| manufacturing_places_tags | object | 19.93 | 190.7 |
| manufacturing_places | str | 18.14 | 41.74 |
| max_imgid | int32 | 75.87 | 35.37 |
| minerals_tags | object | 43.44 | 290.54 |
| misc_tags | object | 100.0 | 530.6 |
| new_additives_n | float64 | 0.01 | 35.37 |
| no_nutrition_data | object | 13.62 | 113.34 |
| nova_group | int32 | 24.6 | 35.37 |
| nova_groups_tags | object | 99.06 | 526.63 |
| nova_groups | str | 24.6 | 37.02 |
| nucleotides_tags | object | 43.44 | 290.54 |
| nutrient_levels_tags | object | 99.06 | 526.63 |
| nutriments | object | 77.08 | 433.3 |
| nutriscore_grade | str | 99.06 | 58.99 |
| nutriscore_score | int32 | 29.79 | 35.37 |
| nutrition_data_per | str | 50.11 | 46.14 |
| obsolete | bool | 100.0 | 4.42 |
| origins_tags | object | 20.12 | 191.53 |
| origins | str | 18.14 | 37.68 |
| owner_fields | object | 2.4 | 116.31 |
| owner | str | 2.44 | 37.64 |
| packagings_complete | bool | 10.2 | 111.53 |
| packaging_recycling_tags | object | 99.07 | 526.65 |
| packaging_shapes_tags | object | 99.07 | 526.65 |
| packaging_tags | object | 15.49 | 171.86 |
| packaging_text | object | 100.0 | 530.6 |
| packaging | str | 15.47 | 42.67 |
| packagings | object | 99.07 | 526.66 |
| photographers | object | 0.1 | 106.53 |
| popularity_key | int64 | 100.0 | 35.37 |
| popularity_tags | object | 33.46 | 248.16 |
| product_name | object | 100.0 | 530.6 |
| product_quantity_unit | str | 26.83 | 37.3 |
| product_quantity | str | 30.47 | 41.41 |
| purchase_places_tags | object | 19.1 | 187.21 |
| quantity | str | 38.94 | 43.52 |
| rev | int32 | 100.0 | 35.37 |
| scans_n | int32 | 33.59 | 35.37 |
| serving_quantity | str | 31.73 | 40.65 |
| serving_size | str | 32.18 | 51.02 |
| states_tags | object | 100.0 | 530.6 |
| stores_tags | object | 24.71 | 211.0 |
| stores | str | 21.6 | 40.07 |
| traces_tags | object | 99.07 | 526.66 |
| unique_scans_n | int32 | 33.59 | 35.37 |
| unknown_ingredients_n | int32 | 27.96 | 35.37 |
| unknown_nutrients_tags | object | 91.24 | 493.43 |
| vitamins_tags | object | 43.44 | 290.54 |
| with_non_nutritive_sweeteners | float64 | 0.68 | 35.37 |
| with_sweeteners | float64 | 0.1 | 35.37 |
| schema_version | int32 | 100.0 | 17.69 |
 
 
Seront conservés les colonnes suivantes
 
### Métier
- code
 
Le code bar du produit, sera utilisé pour identifié le produit de manière unique à partir des requête interne OU d'un scan en magasin
 
### Affichage
- product_name
 
Le nom du produit. La version "lang": "fr" sera utilisé lorsqu'elle est disponnible, dans le cas contraire, "lang": "main sera choisie"
- brands
 
    La marque du produit, purement informationelle
- images
 
    Les images du produit, serviront à enrichir l'interface utilisateur de l'application
 
### Précision
- completeness
 
Utiliser pour estimer la complétude des informations d'un produit
 
### Modèle
- food_groups_tags
 
Utile pour déterminer les rayon aux quels s'appliquent un produit
 
- nutriscore_grade
 
La note nutriscore calculer par OFF
 
- nutriments
 
La liste et les valeurs des nutriments d'un produit afin d'enrichir le modèle pour les sugestions d'alternative
 
 
# Rayons des produits
 
Basé sur l'échantillon des produits en France (1274999 produits), la distibution pas rayon est la suivante
 
 
| Nom | Nombre de produits |
| --- | --- |
| unknown |  |  |  |    714794 |
| en:sugary-snacks |  |     118762 |
| en:fish-meat-eggs |  |     99372 |
| en:milk-and-dairy-products | 64075 |
| en:cereals-and-potatoes |    58625 |
| en:beverages |  |  |     47642 |
| en:fruits-and-vegetables |   40857 |
| en:fats-and-sauces |  |    39839 |
| en:composite-foods |  |    39521 |
| en:salty-snacks |  |  |  30939 |
| en:alcoholic-beverages |     18020 |
| en:baby-foods-and-milks |     2553 |
 
 
Après exclusion du rayon "unknown", il existe donc 11 rayons
 
Dans un premier temps, je m'étais arrêté sur un total de 5 rayon à cause de l'écart entre "beverages" & "fruits-and-vegetables" donnant un palier de 7000 produits
 
Puis, la faible différence de produits entre "fruits-and-vegetables" & "fats-and-sauces" (1018) m'a fais revoir mon idée aussi 8 rayons seront inclut dans l'application
 
A noter que le nombre de rayon sera appliquer sous forme de variable de configuration permetant de modifier la couverture après modificaion de la configuration global du projet
 
 
Afin d'avité les problèmes d'ordre légaux, seront également retiré des donnés les produits dont le nutriscore n'a pas été renseigné
 
| nutriscore_grade | unknown | e | d | c | a | b | not-applicable | graded | graded |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
count | 737807 | 133960 | 124387 | 98108 | 63944 | 49895 | 42499 | 470294 |  37.61 |
 
Offrant un ratio de 37.61 sur le nombre des produits
 
 
Enfin une étude de complétudes (completeness) sur les rayons choisis donne une moyenne proche de 0.6 et un Q2 autours de 0.59
 
Le seuil de complétude minimal par produit sera définie à 50%
 
Encore une fois, cette valeure sera imputé dans le conf afin d'être motifiable sans ré-écriture du code.
 
 
Au finale, ce qui donne sur les rayons choisi
 
| rayon                      |   count |     mean |      std |    25% |    50% |    75% |   min |   max |   valid |   valid_pct |
|:---------------------------|--------:|---------:|---------:|-------:|-------:|-------:|------:|------:|--------:|------------:|
| en:sugary-snacks           |  118762 | 0.613382 | 0.193274 | 0.475  | 0.5875 | 0.7875 |   0.1 |   1.1 |   74835 |       63.01 |
| en:fish-meat-eggs          |   99372 | 0.605946 | 0.219185 | 0.4625 | 0.575  | 0.775  |   0.1 |   1.1 |   56520 |       56.88 |
| en:milk-and-dairy-products |   64075 | 0.646356 | 0.224421 | 0.475  | 0.6    | 0.8    |   0.1 |   1.1 |   41370 |       64.56 |
| en:cereals-and-potatoes    |   58625 | 0.650382 | 0.194464 | 0.475  | 0.675  | 0.7875 |   0.1 |   1.1 |   41548 |       70.87 |
| en:composite-foods         |   39521 | 0.672461 | 0.206732 | 0.475  | 0.675  | 0.8    |   0.1 |   1.1 |   28334 |       71.69 |
| en:beverages               |   47642 | 0.659782 | 0.180807 | 0.55   | 0.675  | 0.7875 |   0.1 |   1.1 |   36092 |       75.76 |
| en:fats-and-sauces         |   39839 | 0.606496 | 0.195341 | 0.475  | 0.575  | 0.775  |   0.1 |   1.1 |   23902 |       60    |
| en:fruits-and-vegetables   |   40857 | 0.624437 | 0.212894 | 0.475  | 0.6    | 0.7875 |   0.1 |   1.1 |   26055 |       63.77 |
 