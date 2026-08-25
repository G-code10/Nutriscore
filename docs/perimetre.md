# TP2 - Profiling & périmètre
<hr>

## Périmètre retenu
<hr>

<pre>

[Colonnes retenues]
[Exemple de donnée] 
[Raison du choix / Critère]

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
[
  {
    "name": "saturated-fat",
    "value": null,
    "100g": 10,
    "serving": null,
    "unit": "g",
    "prepared_value": null,
    "prepared_100g": null,
    "prepared_serving": null,
    "prepared_unit": null
  }, 
  ...
]

<strong>nutriscore_grade</strong>
e
Grade du nutriscore, pas besoin d'argumenté

<strong>nutriscore_score</strong>
25
Nutriscore, pas besoin d'argumenté

<strong>obsolete</strong>
false / true
Nous permet de filtrer directement les produits obsolètes.

<strong>origins_tags</strong>
...

<strong>packaging_recycling_tags</strong>
[
  "en:recycle-in-sorting-bin"
]
eco responsable

<strong>packaging_shapes_tags</strong>
[
  "en:jar",
  "en:lid"
]
Rappel de comment trier le packaging

<strong>popularity_tags</strong>
[
  "top-75-percent-scans-2024",
  "top-80-percent-scans-2024",
  "top-85-percent-scans-2024",
  "top-90-percent-scans-2024",
  "top-1000-sg-scans-2024",
  "top-5000-sg-scans-2024",
  "top-10000-sg-scans-2024",
  "top-50000-sg-scans-2024",
  "top-100000-sg-scans-2024",
  "top-country-sg-scans-2024",
  "top-75-percent-scans-2025",
  "top-80-percent-scans-2025",
  "top-85-percent-scans-2025",
  "top-90-percent-scans-2025",
  "top-50000-gb-scans-2025",
  "top-100000-gb-scans-2025",
  "top-country-gb-scans-2025"
]

<strong>product_name</strong>
[
  {
    "lang": "main",
    "text": "Véritable pâte à tartiner noisettes chocolat noir"
  },
  {
    "lang": "fr",
    "text": "Véritable pâte à tartiner noisettes chocolat noir"
  }
]
Le nom de notre produit c'est important.

<strong>product_quantity</strong>
350

<strong>quantity</strong>
350 g
Hésitation avec la quantité et la quantité du produit, celle-ci a le "g" et l'autre non.
Les deux peuvent être complémentaire.

<strong>states_tags</strong>
[
  "en:to-be-completed",
  "en:nutrition-facts-completed",
  "en:ingredients-completed",
  "en:expiration-date-completed",
  "en:packaging-code-to-be-completed",
  "en:characteristics-to-be-completed",
  "en:origins-to-be-completed",
  "en:categories-completed",
  "en:brands-completed",
  "en:packaging-to-be-completed",
  "en:quantity-completed",
  "en:product-name-completed",
  "en:photos-to-be-validated",
  "en:packaging-photo-to-be-selected",
  "en:nutrition-photo-selected",
  "en:ingredients-photo-selected",
  "en:front-photo-selected",
  "en:photos-uploaded"
]
Permet d'identifier les cases manquantes d'un produits assez rapidement.

<strong>vitamins_tags</strong>
[
  "en:vitamin-e",
  "en:dl-alpha-tocopheryl-acetate",
  "en:retinyl-palmitate",
  "en:cholecalciferol"
]
Un plus

</pre>

## Ce qu'on écarte et pourquoi
<hr>
<pre>

[Colonnes écartées]
[Exemple de donnée] 
[Pourquoi]
</pre>