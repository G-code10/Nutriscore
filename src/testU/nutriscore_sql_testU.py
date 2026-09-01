import sys

sys.path.append(".")

import nutriscore_sql
from conf import sql_conf_dict as conf

# passwd = input("Mot de passe de connexion: ")

values = ["Super U", "Carrouf", "E Lepretre"]

NSQL = nutriscore_sql.NutriscoreSQL(conf, "simirblaiti")

for brand in values:
    NSQL.send_query("INSERT INTO marques (nom) VALUES (%s);", (brand,))

NSQL.send_query("SELECT * from MARQUES;")
rows = NSQL.fetch()
for r in rows:
    print(r)

for brand in values:
    NSQL.send_query("DELETE FROM marques WHERE nom = %s;", (brand,))

NSQL.send_query("SELECT * from MARQUES;")
rows = NSQL.fetch()
for r in rows:
    print(r)
