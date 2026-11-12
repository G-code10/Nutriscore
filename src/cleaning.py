import numpy as np
import pandas as pd

KJ_PER_KCAL = 4.184       # 1 kcal = 4,184 kJ
SALT_PER_SODIUM = 2.5     # sel = sodium x 2,5

NUTRISCORE_GRADES = ["a", "b", "c", "d", "e"]

# Valeur maximale plausible pour 100 g (énergie en kcal, le reste en grammes)
NUTRIENT_MAX = {
    "energy-kcal_100g": 950,
    "fat_100g": 100,
    "saturated-fat_100g": 100,
    "carbohydrates_100g": 100,
    "sugars_100g": 100,
    "fiber_100g": 100,
    "proteins_100g": 100,
    "salt_100g": 100,
}

def get_first_brand(brands):
    """Renvoie la premère marque d'un produit en minuscule, sans espaces sur les côtés et des espaces égaux à l'intérieur du texte ' '."""
    if not isinstance(brands, str):
        return None
    list_brands = [" ".join(brand.split()).lower() for brand in brands.split(',')]
    list_brands = [x for x in list_brands if x]
    if list_brands == []:
        return None
    return list_brands[0]

def flatten_nutriments(nutriment_list):
    """Créer un dictionnaire plat des nutriments à partir d'une liste"""
    if not isinstance(nutriment_list, (np.ndarray, list)):
        return {}
    
    flat_dict = {}

    for nutriment in nutriment_list:
        name = nutriment['name'] + '_100g'
        flat_dict[name] = nutriment['100g']

    return flat_dict

def flatten_categories(category_list):
    """Créer un dictionnaire plat des nutriments à partir d'une liste"""
    if not isinstance(category_list, (np.ndarray, list)):
        return {}
    
    flat_dict = {}

    for category in category_list:
        name = category[3:] # Commencer la lecteur de la chaîne de caractère par le 3
        flat_dict[name] = 1 # Pas besoin d'ajouter +=1 à chaque fois car je souhaite mettre uniquement les unique.

    return flat_dict

def flattening_nutriments_column_join_and_drop(df_column, df, columns_drop:list=None) :
    """
    - Applatissement d'une colonne en un nouveau df_norm
    - df.join(df_norm)
    - Suppression des colonnes 'doublons' (optionnel)
    """
    # Applatir mon dict en nouvelles colonnes.
    df_norm = pd.json_normalize(df_column)

    # Joindre mon df et mes nouvelles colonnes en gardant.
    df_join = df.join(df_norm[['fiber_100g','proteins_100g','energy_100g','saturated-fat_100g','sugars_100g', 'salt_100g']]) # Attention pas de .fillna(0.0) car cela pourrait fausser la décision de la donnée manquante.

    # Retirer les colonnes si la donnée n'est pas vide.
    if columns_drop is not None :
        try: 
            df_join = df_join.drop(columns_drop, axis=1)
        except Exception as e:
            print(f"erreur : {e}")
        
    return df_join

def flattening_categories_column_join_and_drop(df_column, df, columns_drop:list=None) :
    """
    - Applatissement d'une colonne en un nouveau df_norm
    - df.join(df_norm)
    - Suppression des colonnes 'doublons' (optionnel)
    """
    # Applatir mon dict en nouvelles colonnes.
    df_norm = pd.json_normalize(df_column)

    # Joindre mon df et mes nouvelles colonnes en gardant.
    df_join = df.join(df_norm) # Attention pas de .fillna(0.0) car cela pourrait fausser la décision de la donnée manquante.

    # Retirer les colonnes si la donnée n'est pas vide.
    if columns_drop is not None :
        try: 
            df_join = df_join.drop(columns_drop, axis=1)
        except Exception as e:
            print(f"erreur : {e}")
        
    return df_join

def clean_nutriscore_grade(grades):
    """
    Garde les Nutri-Scores valides (a à e), remplace tout le reste par NaN.

    grades : une colonne pandas (Series) de Nutri-Scores.
    Renvoie une nouvelle colonne, sans modifier celle reçue.

    Exemple : ["a", "unknown", "not-applicable"] -> ["a", NaN, NaN]
    """
    grades = grades.map(lambda g: g.strip().lower() if isinstance(g, str) else g)
    return grades.where(grades.isin(NUTRISCORE_GRADES))


def bound_values(values, max_value):
    """
    Remplace par NaN les valeurs négatives ou supérieures à `max_value`.
    Les bornes 0 et `max_value` sont acceptées.

    values : une colonne pandas (Series) de nombres.
    Renvoie une nouvelle colonne, sans modifier celle reçue.

    Exemple avec max_value=100 : [50, -3, 120] -> [50, NaN, NaN]
    """
    return values.where((values >= 0) & (values <= max_value))


def deduplicate_codes(df):
    """
    Garde une seule ligne par code-barres : la plus remplie.
    À remplissage égal, la première ligne rencontrée est gardée.

    df : un DataFrame avec une colonne "code".
    Renvoie un nouveau DataFrame, sans modifier celui reçu.
    """
    return (
        df.assign(not_na_count=df.notna().sum(axis=1))
        .sort_values("not_na_count", ascending=False, kind="stable")
        .drop_duplicates("code")
        .drop(columns="not_na_count")
    )


def clean_empty_lists(values):
    """
    Remplace les listes vides et les valeurs absentes par NaN.
    Les listes non vides sont gardées telles quelles.

    values : une colonne pandas (Series) de listes, comme categories_tags.
    Renvoie une nouvelle colonne, sans modifier celle reçue.

    Exemple : [["en:snacks"], [], None] -> [["en:snacks"], NaN, NaN]
    """
    return values.map(lambda v: v if isinstance(v, (list, np.ndarray)) and len(v) > 0 else np.nan)


def fill_energy_kcal(kcal, kj):
    """
    Complète les kcal manquantes à partir des kJ (kcal = kJ / 4,184).
    Les kcal déjà présentes ne sont jamais modifiées.

    kcal, kj : deux colonnes pandas (Series) alignées sur les mêmes produits.
    Renvoie une nouvelle colonne de kcal, sans modifier celles reçues.

    Exemple : kcal [250, NaN], kJ [2000, 418.4] -> [250, 100]
    """
    return kcal.fillna(kj / KJ_PER_KCAL)


def fill_salt(salt, sodium):
    """
    Complète le sel manquant à partir du sodium (sel = sodium x 2,5).
    Le sel déjà présent n'est jamais modifié.

    salt, sodium : deux colonnes pandas (Series) alignées sur les mêmes produits.
    Renvoie une nouvelle colonne de sel, sans modifier celles reçues.

    Exemple : sel [1.2, NaN], sodium [0.1, 0.4] -> [1.2, 1.0]
    """
    return salt.fillna(sodium * SALT_PER_SODIUM)

# Tolérances des contrôles de cohérence (arrondis des étiquettes)
SUGARS_TOLERANCE = 0.5    # g : sucres jusqu'à 0,5 g au-dessus des glucides
TOTAL_MAX = 105           # g : nutriments pour 100 g, 5 g de marge
FAT_MIN_FOR_ENERGY = 5    # g : 5 g de graisses = au moins 45 kcal
MACRO_COLUMNS = ["fat_100g", "carbohydrates_100g", "proteins_100g", "salt_100g"]

def flag_incoherent(df):
    """
    Signale les produits dont les nutriments sont impossibles entre eux.
    Une valeur manquante ne rend jamais un produit incohérent.

    df : un DataFrame avec les colonnes de nutriments pour 100 g.
    Renvoie une colonne True / False, sans modifier le DataFrame reçu.

    Exemple : sucres 30 g et glucides 10 g -> True
    """
    sugars_above_carbs = df["sugars_100g"] > df["carbohydrates_100g"] + SUGARS_TOLERANCE
    macro_sum = df[MACRO_COLUMNS].sum(axis=1)
    total_above_max = macro_sum > TOTAL_MAX
    zero_kcal_with_fat = (df["energy-kcal_100g"] == 0) & (df["fat_100g"] >= FAT_MIN_FOR_ENERGY)
    return sugars_above_carbs | total_above_max | zero_kcal_with_fat


def prepare_data(df):
    """
    Applique toutes les règles de nettoyage au périmètre, dans l'ordre.

    df : le DataFrame du périmètre (data/food_perimeter.parquet).
    Renvoie un nouveau DataFrame nettoyé, sans modifier celui reçu.
    """
    df = df.copy()

    # 1. Unités : compléter ce qui peut être calculé, AVANT de borner,
    #    pour qu'une valeur convertie absurde soit elle aussi rejetée.
    #    Les colonnes kJ et sodium ne sont pas encore dans le périmètre.
    if "energy-kj_100g" in df.columns:
        df["energy-kcal_100g"] = fill_energy_kcal(df["energy-kcal_100g"], df["energy-kj_100g"])
    if "sodium_100g" in df.columns:
        df["salt_100g"] = fill_salt(df["salt_100g"], df["sodium_100g"])

    # 2. Bornage : valeurs impossibles -> NaN
    for col, max_value in NUTRIENT_MAX.items():
        df[col] = bound_values(df[col], max_value)

    # 3. Nutri-Score, catégories, marque
    df["nutriscore_grade"] = clean_nutriscore_grade(df["nutriscore_grade"])
    df["categories_tags"] = clean_empty_lists(df["categories_tags"])
    df["brand"] = df["brands"].apply(get_first_brand)

    # 4. Doublons EN DERNIER : "la ligne la plus remplie" se mesure
    #    sur des valeurs déjà nettoyées.
    df = deduplicate_codes(df)

    # 5. Drapeau de fiabilité : calculé sur les valeurs finales, rien n'est supprimé
    df["is_incoherent"] = flag_incoherent(df)
    return df
