import psycopg2

## @package NutriscoreSQL
# @brief Connection and query module for postresql server
# @details This module manage the connexion to a postgresql server and the miscaleous queries require for the Nutriscope app

class NutriscoreSQL:
      """! class de gestion et de requêtages du serveur PostgreSQL"""

      def __init__(self, conf : dict, password : str):
            """! Constructeur NutriscoreSQL"""

            if not isinstance(conf, dict) or not isinstance(password, str):
                  raise TypeError("Invalid input parameters format.")

            try:
                  self.__conn = psycopg2.connect(database = conf["database"], 
                                                user = conf["user"], 
                                                host = conf["host"],
                                                password = password,
                                                port = conf["port"])
            except psycopg2.OperationalError as e:
                  raise ConnectionError(f"Impossible de se connecter à PostgreSQL: {e}")
            
            self.__debug = conf.get("debug", False)
            self.__cur = self.__conn.cursor()

      def send_query(self, query : str, params : tuple = ()):
            """! Envoie une requête SQL au serveur courrant"""

            if self.__debug:
                  print(f"Envoie de la requête: {query}")

            self.__cur.execute(query, params)
            self.__conn.commit()

      def send_file(self, file_path : str):
            """! Envoie le contenue d'un fichier SQL au serveur courrant"""

            with open(file_path, "r", encoding="utf-8") as file:
                  sql = file.read()

            self.__cur.execute(sql)
            self.__conn.commit()

      def fetch(self):
            """! Récupère l'itérateur de la dernière requête envoyé"""
            rows = self.__cur.fetchall()

            if self.__debug:
                  print(rows)

            return rows

      def __str__(self):
            return "NutriscoreSQL class"
