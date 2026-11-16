import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SAVING_PATH = PROJECT_ROOT / "data" / "outputs"
SAVING_PATH.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import pandas as pd

from src.cleaning import prepare_data

# Noms des rayons à l'affichage (la base garde "en:...", comme décidé au TP4)
FOOD_GROUP_LABELS = {
    "en:sugary-snacks": "Snacks sucrés",
    "en:salty-snacks": "Snacks salés",
    "en:beverages": "Boissons",
    "en:fruits-and-vegetables": "Fruits et légumes",
    "en:milk-and-dairy-products": "Produits laitiers",
    "en:cereals-and-potatoes": "Céréales et pommes de terre",
    "en:composite-foods": "Plats composés",
    "en:fats-and-sauces": "Matières grasses et sauces",
    "en:fish-meat-eggs": "Viande, poisson, œufs",
}

df = prepare_data(pd.read_parquet(PROJECT_ROOT / "data" / "food_perimeter.parquet"))
df["rayon"] = df["food_group"].map(FOOD_GROUP_LABELS)

sugar = df.groupby("rayon")["sugars_100g"].median()
sugar = sugar.sort_values()

e = sugar['Snacks sucrés'] // sugar['Boissons']
fig, ax = plt.subplots(figsize=(8,5))
ax.barh(sugar.index, sugar.values)
ax.set_title(f"Les snacks sucrés contiennent {e} fois plus de sucres que les boissons")
ax.set_xlabel("Médiane en gramme (g) du sucre par rayon")
fig.tight_layout()
print('Création du graphique 2.1')
fig.savefig(SAVING_PATH / "g_2_1_sucre_par_rayon.png")
plt.close()

df["note"] = df["nutriscore_grade"].map({"a": 1, "b": 2, "c": 3, "d": 4, "e": 5})

cols = ["energy-kcal_100g", "fat_100g", "saturated-fat_100g", "carbohydrates_100g",
        "sugars_100g", "fiber_100g", "proteins_100g", "salt_100g"]

corr = {}
for rayon, groupe in df.groupby("rayon"):
    corr[rayon] = groupe[cols + ['note']].corr(method="spearman")['note']

corr = pd.DataFrame(corr).T
corr = corr.drop(columns='note')
corr = corr.rename(columns={
    'energy-kcal_100g' : "energy",
    'fat_100g' : "fat",
    'saturated-fat_100g' : "saturated-fat",
    'carbohydrates_100g' : "carbohydrates",
    'sugars_100g' : "sugars",
    'fiber_100g' : "fiber",
    'proteins_100g' : "proteins",
    'salt_100g' : "salt",
})

fig, ax = plt.subplots(figsize=(11, 6))
image = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)

ax.set_xticks(range(len(corr.columns)), corr.columns, rotation=30, ha="right")
ax.set_yticks(range(len(corr.index)), corr.index)
ax.set_title("Dans chaque rayon, c'est un nutriment différent qui fait la note")
for i in range(len(corr.index)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")

ax.set_xlabel("1 : plus il y en a, plus la note est mauvaise \n0 : aucun lien\n-1 : plus il y en a, meilleure est la note")
fig.colorbar(image)
fig.tight_layout()
print('Création du graphique 6.1')
fig.savefig(SAVING_PATH / "g_6_1_correlation_nutriscore.png")
plt.close()