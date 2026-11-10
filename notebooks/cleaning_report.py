"""
NutriScope - TP9 : rapport avant/après du nettoyage.

Applique les règles de src/cleaning.py une par une, dans le même ordre que
prepare_data, compte ce que chacune modifie, puis écrit docs/data/rapport_nettoyage.md.

Lancement, depuis la racine du projet :
    .venv\\Scripts\\python.exe -m notebooks.cleaning_report
"""

from datetime import date
from pathlib import Path

import pandas as pd

from src.cleaning import (
    NUTRIENT_MAX,
    bound_values,
    clean_empty_lists,
    clean_nutriscore_grade,
    deduplicate_codes,
    fill_energy_kcal,
    fill_salt,
    get_first_brand,
    prepare_data,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERIMETER_PATH = PROJECT_ROOT / "data" / "food_perimeter.parquet"
REPORT_PATH = PROJECT_ROOT / "docs" / "data" / "rapport_nettoyage.md"


# ---------------------------------------------------------------------------
# Comptages
# ---------------------------------------------------------------------------

def count_emptied(before, after):
    """Nombre de valeurs présentes avant et vides après."""
    return int((before.notna() & after.isna()).sum())


def count_filled(before, after):
    """Nombre de valeurs vides avant et présentes après."""
    return int((before.isna() & after.notna()).sum())


def count_rewritten(before, after):
    """Nombre de valeurs présentes avant et après, mais différentes."""
    both = before.notna() & after.notna()
    return int((before[both] != after[both]).sum())


def fmt(number):
    """1234567 -> '1 234 567' (séparateur de milliers à la française)."""
    return f"{number:,}".replace(",", " ")


# ---------------------------------------------------------------------------
# Application des règles, une par une
# ---------------------------------------------------------------------------

def apply_rules_with_counts(df):
    """
    Applique les règles dans l'ordre de prepare_data et compte leurs effets.
    Renvoie (le DataFrame nettoyé, la liste des lignes du rapport, les règles non appliquées).
    """
    df = df.copy()
    rows = []
    skipped = []

    # 1. Unités
    if "energy-kj_100g" in df.columns:
        new = fill_energy_kcal(df["energy-kcal_100g"], df["energy-kj_100g"])
        rows.append(("fill_energy_kcal", "energy-kcal_100g", "complétées depuis les kJ", count_filled(df["energy-kcal_100g"], new)))
        df["energy-kcal_100g"] = new
    else:
        skipped.append("fill_energy_kcal : colonne `energy-kj_100g` absente du périmètre")

    if "sodium_100g" in df.columns:
        new = fill_salt(df["salt_100g"], df["sodium_100g"])
        rows.append(("fill_salt", "salt_100g", "complétées depuis le sodium", count_filled(df["salt_100g"], new)))
        df["salt_100g"] = new
    else:
        skipped.append("fill_salt : colonne `sodium_100g` absente du périmètre")

    # 2. Bornage
    for col, max_value in NUTRIENT_MAX.items():
        new = bound_values(df[col], max_value)
        rows.append(("bound_values", col, f"hors de [0 ; {max_value}] -> vide", count_emptied(df[col], new)))
        df[col] = new

    # 3. Nutri-Score, catégories, marque
    new = clean_nutriscore_grade(df["nutriscore_grade"])
    rows.append(("clean_nutriscore_grade", "nutriscore_grade", "hors a-e -> vide", count_emptied(df["nutriscore_grade"], new)))
    rows.append(("clean_nutriscore_grade", "nutriscore_grade", "majuscules / espaces corrigés", count_rewritten(df["nutriscore_grade"], new)))
    df["nutriscore_grade"] = new

    new = clean_empty_lists(df["categories_tags"])
    rows.append(("clean_empty_lists", "categories_tags", "liste vide -> vide", count_emptied(df["categories_tags"], new)))
    df["categories_tags"] = new

    df["brand"] = df["brands"].apply(get_first_brand)
    rows.append(("get_first_brand", "brand", "marque extraite", int(df["brand"].notna().sum())))
    rows.append(("get_first_brand", "brand", "sans marque exploitable", int(df["brand"].isna().sum())))

    # 4. Doublons
    before = len(df)
    df = deduplicate_codes(df)
    rows.append(("deduplicate_codes", "code", "lignes en double supprimées", before - len(df)))

    return df, rows, skipped


# ---------------------------------------------------------------------------
# Rapport Markdown
# ---------------------------------------------------------------------------

def build_report(raw, cleaned, rows, skipped):
    """Construit le texte Markdown du rapport."""
    lines = [
        "# Rapport de nettoyage",
        "",
        f"Généré le {date.today():%d/%m/%Y} par `notebooks/cleaning_report.py`, "
        "à partir de `data/food_perimeter.parquet`.",
        "Ne pas modifier à la main : relancer le script pour le mettre à jour.",
        "",
        "## Volumétrie",
        "",
        "| | Lignes | Codes-barres distincts | Marques distinctes |",
        "|---|---|---|---|",
        f"| Avant | {fmt(len(raw))} | {fmt(raw['code'].nunique())} | {fmt(raw['brands'].nunique())} (texte brut) |",
        f"| Après | {fmt(len(cleaned))} | {fmt(cleaned['code'].nunique())} | {fmt(cleaned['brand'].nunique())} |",
        "",
        "## Lignes touchées par règle",
        "",
        "Les règles sont listées dans leur ordre d'application (celui de `prepare_data`).",
        "",
        "| Règle | Colonne | Effet | Valeurs |",
        "|---|---|---|---|",
    ]
    lines += [f"| `{rule}` | `{column}` | {effect} | {fmt(count)} |" for rule, column, effect, count in rows]

    if skipped:
        lines += ["", "**Règles non appliquées :**", ""]
        lines += [f"- {reason}" for reason in skipped]

    lines += [
        "",
        "## Valeurs manquantes des nutriments",
        "",
        "| Colonne | Avant | Après |",
        "|---|---|---|",
    ]
    for col in NUTRIENT_MAX:
        lines.append(f"| `{col}` | {raw[col].isna().mean():.2%} | {cleaned[col].isna().mean():.2%} |")

    return "\n".join(lines) + "\n"


def main():
    raw = pd.read_parquet(PERIMETER_PATH)
    cleaned, rows, skipped = apply_rules_with_counts(raw)

    # Garde-fou : le rapport doit décrire exactement ce que fait prepare_data.
    expected = prepare_data(raw)
    if len(cleaned) != len(expected) or not cleaned.index.equals(expected.index):
        raise RuntimeError("Le rapport ne suit plus prepare_data : mettre à jour apply_rules_with_counts.")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(raw, cleaned, rows, skipped), encoding="utf-8")
    print(f"Rapport écrit dans {REPORT_PATH}")


if __name__ == "__main__":
    main()
