# Rapport de nettoyage

Généré le 10/11/2026 par `notebooks/cleaning_report.py`, à partir de `data/food_perimeter.parquet`.
Ne pas modifier à la main : relancer le script pour le mettre à jour.

## Volumétrie

| | Lignes | Codes-barres distincts | Marques distinctes |
|---|---|---|---|
| Avant | 456 484 | 456 479 | 65 908 (texte brut) |
| Après | 456 479 | 456 479 | 41 339 |

## Lignes touchées par règle

Les règles sont listées dans leur ordre d'application (celui de `prepare_data`).

| Règle | Colonne | Effet | Valeurs |
|---|---|---|---|
| `bound_values` | `energy-kcal_100g` | hors de [0 ; 950] -> vide | 341 |
| `bound_values` | `fat_100g` | hors de [0 ; 100] -> vide | 21 |
| `bound_values` | `saturated-fat_100g` | hors de [0 ; 100] -> vide | 10 |
| `bound_values` | `carbohydrates_100g` | hors de [0 ; 100] -> vide | 33 |
| `bound_values` | `sugars_100g` | hors de [0 ; 100] -> vide | 24 |
| `bound_values` | `fiber_100g` | hors de [0 ; 100] -> vide | 59 |
| `bound_values` | `proteins_100g` | hors de [0 ; 100] -> vide | 11 |
| `bound_values` | `salt_100g` | hors de [0 ; 100] -> vide | 11 |
| `clean_nutriscore_grade` | `nutriscore_grade` | hors a-e -> vide | 34 498 |
| `clean_nutriscore_grade` | `nutriscore_grade` | majuscules / espaces corrigés | 0 |
| `clean_empty_lists` | `categories_tags` | liste vide -> vide | 0 |
| `get_first_brand` | `brand` | marque extraite | 359 217 |
| `get_first_brand` | `brand` | sans marque exploitable | 97 267 |
| `deduplicate_codes` | `code` | lignes en double supprimées | 5 |

**Règles non appliquées :**

- fill_energy_kcal : colonne `energy-kj_100g` absente du périmètre
- fill_salt : colonne `sodium_100g` absente du périmètre

## Valeurs manquantes des nutriments

| Colonne | Avant | Après |
|---|---|---|
| `energy-kcal_100g` | 0.00% | 0.07% |
| `fat_100g` | 0.46% | 0.46% |
| `saturated-fat_100g` | 1.16% | 1.16% |
| `carbohydrates_100g` | 0.47% | 0.47% |
| `sugars_100g` | 0.92% | 0.93% |
| `fiber_100g` | 47.41% | 47.42% |
| `proteins_100g` | 0.33% | 0.33% |
| `salt_100g` | 3.75% | 3.76% |
