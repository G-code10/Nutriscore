import sys

sys.path.append(".")

import nutriscore_sql
from conf import sql_conf_dict as conf

# ceci est notre référence et ne dois pas bouger sans accord de l'équipe
result = []

# Sortie après création des tables
result.append([('id', 'bigint', 'NO', None)
               , ('nom', 'character varying', 'NO', None)])
result.append([('id', 'bigint', 'NO', None)
               , ('nom', 'character varying', 'NO', None)])
result.append([('code', 'bigint', 'NO', None)
               , ('marque_id', 'bigint', 'NO', None)
               , ('nom', 'character varying', 'NO', None)
               , ('lang', 'character varying', 'NO', None)
               , ('fiber', 'double precision', 'YES', None)
               , ('proteins', 'double precision', 'YES', None)
               , ('energy', 'double precision', 'YES', None)
               , ('saturated_fat', 'double precision', 'YES', None)
               , ('sugars', 'double precision', 'YES', None)
               , ('salt', 'double precision', 'YES', None)])
result.append([('id', 'bigint', 'NO', None)
               , ('categorie_id', 'bigint', 'NO', None)
               , ('produit_id', 'bigint', 'NO', None)])

# Sortie après inser/select d'un produit
result.append([(598745298751, 1, 'THE Produit', 'fr', 0.5, 1.25, 3350.0, 0.5, 10.0, 42.0)])

# Sortie après inser/select de marques
result.append([(1, 'Sup-per U')
               , (2, 'Carrouf')
               , (3, 'E Lepretre')])

# Sortie de marques après delete des tables
result.append([])

# Sortie de produits après delete des tables
result.append([])

tables = ["marques", "categories", "produits", "produits_categories"]

def check_output(output, test_id):
    reference = result[test_id]

    if reference == output:
        print(f"Validation du test {test_id}")
    else:
        print(f"Erreur lors du test {test_id}")

    return current_test + 1

sql_db_struct = "../sql/postgre_creation.sql"

values = ["Sup-per U", "Carrouf", "E Lepretre", "E Lepretre"]

NSQL = nutriscore_sql.NutriscoreSQL(conf, "simirblaiti")
NSQL.send_file(sql_db_struct)

current_test = 0
for table in tables:
    NSQL.send_query("""SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = %s
ORDER BY ordinal_position;""", (table,))
    
    current_test = check_output(NSQL.fetch(), current_test)

for brand in values:
    NSQL.send_query("INSERT INTO marques (nom) VALUES (%s);", (brand,))

NSQL.send_query("INSERT INTO produits (code, marque_id, nom, lang, fiber, proteins, energy, saturated_fat, sugars, salt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                ,(598745298751, 1, "THE Produit", "fr", 0.5, 1.25, 3350, 0.5, 10, 42,))

NSQL.send_query("SELECT * from produits;")
current_test = check_output(NSQL.fetch(), current_test)

NSQL.send_query("SELECT * from marques;")
current_test = check_output(NSQL.fetch(), current_test)

NSQL.send_query("DELETE FROM produits;")

for brand in values:
    NSQL.send_query("DELETE FROM marques WHERE nom = %s;", (brand,))

NSQL.send_query("SELECT * from marques;")
current_test = check_output(NSQL.fetch(), current_test)

NSQL.send_query("SELECT * from produits;")
current_test = check_output(NSQL.fetch(), current_test)
