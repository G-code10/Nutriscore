
## @var nutriscope_root_dir
# @brief La racine du l'application installé
nutriscope_root_dir = "C:/Program Files (x86)/Nutriscope"

## @var cache_dir
# @brief Le répertorie de cache
cache_dir = nutriscope_root_dir + "/cache"

## @var off_parquet_url
# @brief L'URL du parquet
# details L'URL ou peut être télécharger le ficheir food.parquet d'OenFoodFact
off_parquet_url = "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet?download=true"

## @var off_parquet_path
# @brief Le nom du fichier parquet
# @details Le nom du fichier parquet pour le stockage local
off_parquet_path = cache_dir + "/food.parquet"

## @var off_parquet_path
# @brief Le nom du fichier parquet
# @details Le nom du fichier parquet pour le stockage local
sql_conf_dict = {
    "database": "nutriscope", 
    "user": "nutriscope_app", 
    "host": "localhost", 
    "port": 5432,
    "debug": False
}
