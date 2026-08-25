# TP2 - Profiling & périmètre
<hr>

## Périmètre retenu
<hr>

<pre>

[Colonnes retenues]
[Exemple de donnée] 
[Raison du choix]

<strong>brands</strong>
Bovetti
Donnée brut, simple texte, importance de connaître la marque. Pour une tracabilité et rassurer la clientèle.

<strong>code</strong>
0000101209159
Donnée brut, simple texte, important pour retrouver la donnée grâce au code-barre

<strong>completeness</strong>
0.7875
Savoir si les informations sont complètes.

<strong>countries_tags</strong>
[
    "en:france"
]
Dans quel pays trouver le produit, pour filtrer c'est important.

<strong>data_quality_errors_tags</strong>
[
    "en:nutrition-value-total-over-105","en:energy-value-in-kcal-does-not-match-value-computed-from-other-nutrients"
]
Récupérer les erreurs pour mettre en avant une erreur de complétion

<strong>entry_dates_tags</strong>
[
  "2017-03-09",
  "2017-03",
  "2017"
]
Fonctionne bien avec l'obsolescence des informations, plus pour le côté gestion des données, sans forcément afficher cette info

<strong>food_groups_tags</strong>
[
  "en:beverages",
  "en:unsweetened-beverages"
]

<strong>images</strong>
[
    {
        "key":"1"
        ... (très long)
    }
]
Permet d'afficher une petite image du produit

<strong>ingredients_analysis_tags</strong>
[
  "en:palm-oil-free",
  "en:maybe-vegan",
  "en:vegetarian"
]
Des informations importantes à récupérer pour l'alimentation de chacun

<strong>ingredients_original_tags</strong>
[
  "en:hazelnut",
  "en:cocoa dark chocolate",
  "en:sugar",
  "en:cocoa-paste",
  "en:sugar",
  "en:cocoa-butter",
  "en:vanilla-extract"
]

<strong>ingredients_tags</strong>
[
  "en:hazelnut",
  "en:nut",
  "en:tree-nut",
  "en:cocoa dark chocolate",
  "en:sugar",
  "en:added-sugar",
  "en:disaccharide",
  "en:cocoa-paste",
  "en:plant",
  "en:cocoa",
  "en:cocoa-butter",
  "en:oil-and-fat",
  "en:vegetable-oil-and-fat",
  "en:vegetable-fat",
  "en:vanilla-extract",
  "en:extract",
  "en:vanilla",
  "en:vegetable-extract"
]
Permet d'établir une liste en cas d'alergène

<strong>ingredients_text</strong>
[
  {
    "lang": "main",
    "text": "HAZELNUTS, 73% cocoa dark chocolate (cocoa mass, sugar, cocoa butter, vanilla extract), sugar, rapeseed oil\r\n\r\nMay contain traces of other nuts, milk, and soy."
  },
  {
    "lang": "en",
    "text": "HAZELNUTS, 73% cocoa dark chocolate (cocoa mass, sugar, cocoa butter, vanilla extract), sugar, rapeseed oil\r\n\r\nMay contain traces of other nuts, milk, and soy."
  },
  {
    "lang": "en",
    "text": "<span class=\"allergen\">HAZELNUTS</span>, 73% cocoa dark chocolate (cocoa mass, sugar, cocoa butter, vanilla extract), sugar, rapeseed oil\r\n\r\nMay contain traces of other <span class=\"allergen\">nuts</span>, <span class=\"allergen\">milk</span>, and <span class=\"allergen\">soy</span>."
  }
]
Permet d'établir une liste en cas d'alergène en récupérant le span .allergen

<strong>ingredients</strong>
Donnée trop longue...
À récupérer à la place des trois précédentes, mais possède énormément de keys et values.

<strong>lang</strong>
fr
Permet de filtrer par langue

<strong>nova_groups_tags</strong>
[
  "en:3-processed-foods" (ultra, unprocessed, processed-minimaly etc...)
]
Savoir si l'aliment est transformé ou non, 

<strong>nutrient_levels_tags</strong>
[
  "en:fat-in-high-quantity",
  "en:saturated-fat-in-high-quantity",
  "en:sugars-in-high-quantity",
  "en:salt-in-low-quantity"
]

<strong>nutriments</strong>


<strong>nutriscore_grade</strong>


<strong>nutriscore_score</strong>


<strong>obsolete</strong>


<strong>origins_tags</strong>


<strong>packaging_recycling_tags</strong>


<strong>packaging_shapes_tags</strong>


<strong>popularity_tags</strong>


<strong>product_name</strong>


<strong>product_quantity</strong>


<strong>quantity</strong>


</pre>

## Périmètre retenu
<hr>

## Périmètre retenu
<hr>