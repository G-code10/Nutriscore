# Sources

## Périmètre France

Nbr de produits : 456_484
14 colonnes : code, product_name, brands, categories_tags, nutriscore_grade, energy-kcal_100g, fat_100g, saturated-fat_100g, carbohydrates_100g, sugars_100g, fiber_100g, proteins_100g, salt_100g, food_group

## Base PostgreSQL

5 tables :
- brands
- categories
- nutriments
- products
- products_categories

## Parquet partitionné

Nbr de produits : 456_479
16 colonnes : code, product_name, brands, categories_tags, nutriscore_grade, energy-kcal_100g, fat_100g, saturated-fat_100g, carbohydrates_100g, sugars_100g, fiber_100g, proteins_100g, salt_100g, food_group, brand, is_incoherent

# Chemin des données

<pre>
NutriScope
    |__data/
    |    |__perimeter_partitioned/
    |    |        |__[rayon]/ x 9 
    |    |              |__[rayon].parquet
    |    |__[***].parquet
    |    |__[***].csv
    |_src/
    |    |__scripts.py
</pre>

# Benchmark (résumé)

| Requête	| CSV + pandas | PostgreSQL	| Parquet + DuckDB |
|---|---|---|---|
| 1. Volumétrie	        | 1,40 s | 	0,083 s	| 0,008 s |
| 2. Complétude	        | 1,40 s | 0,684 s	| 0,011 s |
| 3. Sucre des boissons	| 1,41 s | 0,126 s	| 0,007 s | 

#