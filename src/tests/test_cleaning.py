import pandas as pd
import numpy as np
import pytest
from src.cleaning import get_first_brand, clean_nutriscore_grade, bound_values, deduplicate_codes, clean_empty_lists, fill_energy_kcal, fill_salt

# ---------------------------------------------------------------------------
# get_first_brand
# ---------------------------------------------------------------------------

def test_get_first_brand_normal_split():
    assert get_first_brand("Carrefour BIO, Carrefour") == "carrefour bio"

def test_get_first_brand_no_split():
    assert get_first_brand("Carrefour BIO") == "carrefour bio"

# Test obsolète car cela m'a poussé à changer ma fonction
# def test_get_first_brand_first_char_comma():
#     assert get_first_brand(",Carrefour") is None

def test_get_first_brand_empty_string():
    assert get_first_brand("") is None

def test_get_first_brand_nan():
    assert get_first_brand(np.nan) is None

# Nouveaux test après changement de la fonction
def test_get_first_brand_skips_empty_first_brand():
    assert get_first_brand(",Carrefour") == "carrefour"

def test_get_first_brand_skips_several_empty_brands():
    assert get_first_brand(" , ,Lidl") == "lidl"

def test_get_first_brand_only_commas_returns_none():
    assert get_first_brand(",,") is None

# Correction du TP4 : les espaces multiples fusionnaient mal les marques (41 420 -> 41 339)
def test_get_first_brand_collapses_inner_spaces():
    assert get_first_brand("  Marks   &  Spencer  ") == "marks & spencer"

# ---------------------------------------------------------------------------
# clean_nutriscore_grade
# ---------------------------------------------------------------------------

def test_clean_nutriscore_grade_keeps_valid_letter():
    grades = pd.Series(["a"])
    assert clean_nutriscore_grade(grades).tolist() == ["a"]

def test_clean_nutriscore_grade_keeps_all_valid_letters():
    grades = pd.Series(["a", "b", "c", "d", "e"])
    assert clean_nutriscore_grade(grades).tolist() == ["a", "b", "c", "d", "e"]

def test_clean_nutriscore_grade_unknown_becomes_nan():
    grades = pd.Series(["unknown"])
    assert clean_nutriscore_grade(grades).isna().tolist() == [True]

def test_clean_nutriscore_grade_not_applicable_becomes_nan():
    grades = pd.Series(["not-applicable"])
    assert clean_nutriscore_grade(grades).isna().tolist() == [True]

def test_clean_nutriscore_grade_uppercase():
    grades = pd.Series(["A"])
    assert clean_nutriscore_grade(grades).tolist() == ["a"]

def test_clean_nutriscore_grade_strip():
    grades = pd.Series([" b "])
    assert clean_nutriscore_grade(grades).tolist() == ["b"]

def test_clean_nutriscore_grade_empty_string_becomes_nan():
    grades = pd.Series([""])
    assert clean_nutriscore_grade(grades).isna().tolist() == [True]

def test_clean_nutriscore_grade_nan_stays_nan():
    grades = pd.Series([np.nan])
    assert clean_nutriscore_grade(grades).isna().tolist() == [True]

def test_clean_nutriscore_grade_does_not_modify_input():
    grades = pd.Series(["a", "unknown"])
    clean_nutriscore_grade(grades)
    assert grades.tolist() == ["a", "unknown"]

# ---------------------------------------------------------------------------
# bound_values
# ---------------------------------------------------------------------------

def test_bound_values_keeps_normal_value():
    values = pd.Series([50.0])
    assert bound_values(values, 100).tolist() == [50.0]

def test_bound_values_negative_becomes_nan():
    values = pd.Series([-3.0])
    assert bound_values(values, 100).isna().tolist() == [True]

def test_bound_values_above_max_becomes_nan():
    values = pd.Series([120.0])
    assert bound_values(values, 100).isna().tolist() == [True]

# Cas aux bornes : 0 et le maximum doivent être acceptés
def test_bound_values_keeps_zero():
    values = pd.Series([0.0])
    assert bound_values(values, 100).tolist() == [0.0]

def test_bound_values_keeps_max_value():
    values = pd.Series([100.0])
    assert bound_values(values, 100).tolist() == [100.0]

def test_bound_values_nan_stays_nan():
    values = pd.Series([np.nan])
    assert bound_values(values, 100).isna().tolist() == [True]

# Cas du TP2 : une huile à 929 kcal est plausible (tolérance jusqu'à 950)
def test_bound_values_keeps_oil_energy():
    values = pd.Series([929.0])
    assert bound_values(values, 950).tolist() == [929.0]

# Cas du TP2 : 8 700 kcal pour 100 g est impossible
def test_bound_values_impossible_energy_becomes_nan():
    values = pd.Series([8700.0])
    assert bound_values(values, 950).isna().tolist() == [True]

def test_bound_values_mixed_series():
    values = pd.Series([50.0, -3.0, 120.0, np.nan])
    expected = pd.Series([50.0, np.nan, np.nan, np.nan])
    pd.testing.assert_series_equal(bound_values(values, 100), expected)

def test_bound_values_does_not_modify_input():
    values = pd.Series([50.0, -3.0])
    bound_values(values, 100)
    assert values.tolist() == [50.0, -3.0]

# ---------------------------------------------------------------------------
# deduplicate_codes
# ---------------------------------------------------------------------------

def test_deduplicate_codes_keeps_most_filled_row():
    df = pd.DataFrame({
        "code": ["001", "001"],
        "name": ["Biscuit", "Biscuit"],
        "sugars": [np.nan, 25.0],
    })
    result = deduplicate_codes(df)
    assert len(result) == 1
    assert result["sugars"].iloc[0] == 25.0

def test_deduplicate_codes_without_duplicates_keeps_all_rows():
    df = pd.DataFrame({"code": ["001", "002", "003"], "sugars": [1.0, 2.0, 3.0]})
    assert len(deduplicate_codes(df)) == 3

def test_deduplicate_codes_three_times_same_code():
    df = pd.DataFrame({"code": ["001", "001", "001"], "sugars": [np.nan, 5.0, np.nan]})
    result = deduplicate_codes(df)
    assert len(result) == 1
    assert result["sugars"].iloc[0] == 5.0

def test_deduplicate_codes_two_codes_each_duplicated():
    df = pd.DataFrame({"code": ["001", "002", "001", "002"], "sugars": [1.0, np.nan, np.nan, 2.0]})
    result = deduplicate_codes(df)
    assert sorted(result["code"]) == ["001", "002"]

# À remplissage égal, c'est la première ligne qui est gardée (tri stable)
def test_deduplicate_codes_same_fill_keeps_first_row():
    df = pd.DataFrame({"code": ["001", "001"], "name": ["Premier", "Second"]})
    assert deduplicate_codes(df)["name"].iloc[0] == "Premier"

def test_deduplicate_codes_removes_temporary_column():
    df = pd.DataFrame({"code": ["001", "001"], "sugars": [np.nan, 25.0]})
    assert "not_na_count" not in deduplicate_codes(df).columns

# Défaut du TP4 : df["not_na_count"] = ... modifiait le df reçu
def test_deduplicate_codes_does_not_modify_input():
    df = pd.DataFrame({"code": ["001", "001"], "sugars": [np.nan, 25.0]})
    deduplicate_codes(df)
    assert len(df) == 2
    assert "not_na_count" not in df.columns

# ---------------------------------------------------------------------------
# clean_empty_lists
# ---------------------------------------------------------------------------

def test_clean_empty_lists_keeps_filled_list():
    values = pd.Series([["en:snacks", "en:biscuits"]])
    assert clean_empty_lists(values).iloc[0] == ["en:snacks", "en:biscuits"]

# Dans un fichier Parquet, les listes arrivent sous forme de tableaux numpy
def test_clean_empty_lists_keeps_filled_array():
    values = pd.Series([np.array(["en:snacks"])])
    assert clean_empty_lists(values).iloc[0].tolist() == ["en:snacks"]

def test_clean_empty_lists_empty_list_becomes_nan():
    values = pd.Series([[]])
    assert clean_empty_lists(values).isna().tolist() == [True]

def test_clean_empty_lists_empty_array_becomes_nan():
    values = pd.Series([np.array([])])
    assert clean_empty_lists(values).isna().tolist() == [True]

def test_clean_empty_lists_none_becomes_nan():
    values = pd.Series([None])
    assert clean_empty_lists(values).isna().tolist() == [True]

def test_clean_empty_lists_nan_stays_nan():
    values = pd.Series([np.nan])
    assert clean_empty_lists(values).isna().tolist() == [True]

def test_clean_empty_lists_does_not_modify_input():
    values = pd.Series([[], ["en:snacks"]])
    clean_empty_lists(values)
    assert values.tolist() == [[], ["en:snacks"]]

# ---------------------------------------------------------------------------
# fill_energy_kcal / fill_salt (normalisation des unités)
# ---------------------------------------------------------------------------

# Une valeur saisie n'est jamais écrasée, même si les kJ ne correspondent pas
def test_fill_energy_kcal_keeps_existing_kcal():
    kcal = pd.Series([250.0])
    kj = pd.Series([2000.0])
    assert fill_energy_kcal(kcal, kj).tolist() == [250.0]

def test_fill_energy_kcal_converts_kj_when_kcal_missing():
    kcal = pd.Series([np.nan])
    kj = pd.Series([418.4])
    assert fill_energy_kcal(kcal, kj).iloc[0] == pytest.approx(100.0)

def test_fill_energy_kcal_both_missing_stays_nan():
    kcal = pd.Series([np.nan])
    kj = pd.Series([np.nan])
    assert fill_energy_kcal(kcal, kj).isna().tolist() == [True]

def test_fill_energy_kcal_does_not_modify_input():
    kcal = pd.Series([np.nan])
    fill_energy_kcal(kcal, pd.Series([418.4]))
    assert kcal.isna().tolist() == [True]

def test_fill_salt_keeps_existing_salt():
    salt = pd.Series([1.2])
    sodium = pd.Series([0.1])
    assert fill_salt(salt, sodium).tolist() == [1.2]

def test_fill_salt_converts_sodium_when_salt_missing():
    salt = pd.Series([np.nan])
    sodium = pd.Series([0.4])
    assert fill_salt(salt, sodium).iloc[0] == pytest.approx(1.0)

def test_fill_salt_both_missing_stays_nan():
    salt = pd.Series([np.nan])
    sodium = pd.Series([np.nan])
    assert fill_salt(salt, sodium).isna().tolist() == [True]

def test_fill_salt_does_not_modify_input():
    salt = pd.Series([np.nan])
    fill_salt(salt, pd.Series([0.4]))
    assert salt.isna().tolist() == [True]