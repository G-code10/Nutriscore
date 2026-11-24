import pandas as pd
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

# from src.cleaning import prepare_data
from notebooks.build_perimeter import main as build_perimeter_main, PERIMETER_PATH
# from notebooks.cleaning_report import main as cleaning_report_main
from notebooks.load_database import main as load_base_main
from notebooks.convert_to_parquet import parquet as convert_to_parquet, OUTPUT_PATH
from notebooks.build_features import export_features, FEATURES_PATH
from notebooks.clean_data import cleaning, CLEANED_DATA_PATH

def load():
    build_perimeter_main()
    return len(pd.read_parquet(PERIMETER_PATH))

def clean():
    df = cleaning()
    return len(df)

def load_base():
    df = pd.read_parquet(CLEANED_DATA_PATH)
    load_base_main(df)
    return len(df)

def parquet():
    df = pd.read_parquet(CLEANED_DATA_PATH)
    return convert_to_parquet(df, OUTPUT_PATH)

def export():
    df = pd.read_parquet(OUTPUT_PATH)
    FORCE= "--force" in sys.argv # True si il y est, autrement False
    return export_features(df, FEATURES_PATH, force=FORCE)

STEPS = {
    "charger"       : load,
    "nettoyer"      : clean,
    "charger_base"  : load_base,
    "parquet"       : parquet,
    "exports"       : export,
}

def run(name):
    """Lance une étape, mesure sa durée, affiche le résultat."""
    if not name in STEPS:
        print("Argument invalide, vérifiez le nom : info")
        return False
    
    start = time.perf_counter()
    lines = STEPS[name]()
    print(f"{name:<10} {lines:>7,} lignes   {time.perf_counter() - start:.2f} s")

if __name__ == "__main__" :
    if len(sys.argv) >= 2 :
        asked = sys.argv[1]
    else :
        sys.exit("Arguments manquant, voir : info")
    if asked == "all" :
        for name in STEPS:
            run(name)
    elif asked == "info" :
        for step in STEPS:
            print(f" - {step}")
    else : 
        run(asked)