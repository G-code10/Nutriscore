# TP2 - Profiling & périmètre
<hr>

## Périmètre retenu (avant meeting)
<pre>

[Colonnes retenues]
[Exemple de donnée] 
[Raison du choix / Critère]

<span style="color:green"><strong>allergens_tags</strong></span>
[
  "en:nuts"
]
Afin de pouvoir signaler les différents allergènes présent dans le produit

<span style="color:green"><strong>brands</strong></span>
Bovetti
Donnée brut, simple texte, importance de connaître la marque. Pour une tracabilité et rassurer la clientèle.

<span style="color:green"><strong>categories</strong></span>
Plant-based foods and beverages, Beverages, Hot beverages, Plant-based beverages, Teas, Tea bags
Donnée <strong>très importante</strong>, à compléter pour le calcule du nutriscore

<span style="color:green"><strong>code</strong></span>
0000101209159
Donnée brut, simple texte, important pour retrouver la donnée grâce au code-barre

<span style="color:green"><strong>completeness</strong></span>
0.7875
Savoir si les informations sont complètes.

<span style="color:green"><strong>countries_tags</strong></span>
[
    "en:france"
]
Dans quel pays trouver le produit, pour filtrer c'est important.
<span style="color: red;">
Colonne écartée

<strong>data_quality_errors_tags</strong>
[
    "en:nutrition-value-total-over-105","en:energy-value-in-kcal-does-not-match-value-computed-from-other-nutrients"
]
Récupérer les erreurs pour mettre en avant une erreur de complétion</span>

<span style="color:green"><strong>entry_dates_tags</strong></span>
[
  "2017-03-09",
  "2017-03",
  "2017"
]
Fonctionne bien avec l'obsolescence des informations, plus pour le côté gestion des données, sans forcément afficher cette info

<span style="color:green"><strong>food_groups_tags</strong></span>
[
  "en:beverages",
  "en:unsweetened-beverages"
]

<span style="color:green"><strong>images</strong></span>
[
    {
        "key":"1"
        ... (très long)
    }
]
Permet d'afficher une petite image du produit

<span style="color:green"><strong>ingredients_analysis_tags</strong></span>
[
  "en:palm-oil-free",
  "en:maybe-vegan",
  "en:vegetarian"
]
Des informations importantes à récupérer pour l'alimentation de chacun

<strong>ingredients_original_tags</strong> <span style="color:lightblue">Vérifier avec la prochaine colonne</span>
[
  "en:hazelnut",
  "en:cocoa dark chocolate",
  "en:sugar",
  "en:cocoa-paste",
  "en:sugar",
  "en:cocoa-butter",
  "en:vanilla-extract"
]

<span style="color:green"><strong>ingredients_tags</strong></span>
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

<span style="color:green"><strong>ingredients_text</strong></span>
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

<span style="color:green"><strong>ingredients</strong></span>
Donnée trop longue...
À récupérer à la place des trois précédentes, mais possède énormément de keys et values.

<span style="color:green"><strong>lang</strong></span>
fr
Permet de filtrer par langue

<span style="color:green"><strong>nova_groups_tags</strong></span>
[
  "en:3-processed-foods" (ultra, unprocessed, processed-minimaly etc...)
]
Savoir si l'aliment est transformé ou non, 
<span style="color: red;">
Colonne écartée

<strong>nutrient_levels_tags</strong>
[
  "en:fat-in-high-quantity",
  "en:saturated-fat-in-high-quantity",
  "en:sugars-in-high-quantity",
  "en:salt-in-low-quantity"
]
</span>
<span style="color:green"><strong>nutriments</strong></span>
[
  {
    "name": "saturated-fat",
    "value": null,
    "100g": 10, <span style="color:lightblue">À vérifier</span>
    "serving": null,
    "unit": "g", <span style="color:lightblue">À vérifier</span>
    "prepared_value": null,
    "prepared_100g": null,
    "prepared_serving": null,
    "prepared_unit": null
  }, 
  ...
]

<span style ="color:green"><strong>nutriscore_grade</strong></span>
e
Grade du nutriscore, pas besoin d'argumenté

<span style ="color:green"><strong>nutriscore_score</strong></span>
25
Nutriscore, pas besoin d'argumenté

<span style ="color:green"><strong>obsolete</strong></span>
false / true
Nous permet de filtrer directement les produits obsolètes.

<strong>origins_tags</strong> <span style="color:lightblue">Vérifier l'info</span>
...

<span style="color:green"><strong>packaging_recycling_tags</strong></span> <span style="color:yellow">Selon la décision du client</span>
[
  "en:recycle-in-sorting-bin"
]
eco responsable

<span style="color:green"><strong>packaging_shapes_tags</strong></span> <span style="color:yellow">Selon la décision du client</span>
[
  "en:jar",
  "en:lid"
]
Rappel de comment trier le packaging



<span style="color:green"><strong>popularity_tags</strong></span> <span style="color: yellow;">Selon la décision du client</span>
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

<span style="color:green"><strong>product_name</strong></span>
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

<span style="color:green"><strong>product_quantity</strong></span>
350

<span style="color:green"><strong>product_quantity_unit</strong></span>
g
<span style="color: red;">
Colonne écartée

<strong>quantity</strong>
350 g
Hésitation avec la quantité et la quantité du produit, celle-ci a le "g" et l'autre non.
Les deux peuvent être complémentaire.</span>

<span style="color:green"><strong>states_tags</strong></span>
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

<strong>vitamins_tags</strong> <span style="color:lightblue">Vérifier si l'info n'est pas ailleurs <span style="color:lightgreen">UPDATE : info dans ingredients_tags, MAIS pas les même vitamines, problème de cohérence des informations</span></span>
[
  "en:vitamin-e",
  "en:dl-alpha-tocopheryl-acetate",
  "en:retinyl-palmitate",
  "en:cholecalciferol"
]
Un plus
</pre>

## <span style="color:red">Ce qu'on écarte et pourquoi</span>

<pre>

[Colonnes écartées]
[Pourquoi]

<strong>Filtre après meeting :</strong>
['data-quality-errors-tags','nutrient_levels_tags', quantity]
Écartées après un premier meeting pour cause que les données présentées peuvent être calculées par nos soins au lieu de faire confiance à l'entrée ou la récupération de ces données.

<strong>Information non pertinente :</strong>
[exemple : 'created_t', 'creator', 'last_editor', ...]
Pas nécessaire de garder ces colonnes pour connaître qui a ajouté ce produit ou l'a édité.

<strong>Doublons :</strong>
['countries', 'countries_tags']
Ce genre d'exemple, nous avons préféré prendre seulement une sur les deux, car cela faisait énormément de redondances dans les données
</pre>

## Décision de périmètre

### Rayons couverts au lancement & colonnes concervées

#### Vitamines
<pre>
vitamin-a
vitamin-b1
vitamin-b2
vitamin-b6
vitamin-b9
vitamin-b12
vitamin-c
vitamin-d
vitamin-e
vitamin-k
vitamin-pp
vitamine-h
</pre>
#### Énergie
<pre>
energy
energy-kj
energy-kcal
</pre>
#### Valeur nutritionnelle
<pre>
fat
saturated-fat
carbohydrates
sugars
fiber
proteins
salt
sodium
cholesterol
</pre>
#### Minéraux
<pre>
calcium
iron
magnesium
potassium
zinc
</pre>
#### Oméga
<pre>
omega-3-fat
omega-6-fat
omega-9-fat
</pre>
#### Écologie - Recyclage
<pre>
packaging_recycling_tags
packaging_shapes_tags
</pre>
#### Autres...
<pre>
caffeine
alcohol
water
</pre>

### Seuil de complétude minimal par produit
<pre>
Minimum : 0.0
Maximum : 1.1 (?)
Moyenne : 0.4133
Médiane : 0.375

Ce qui veut dire que l'on doit choisir un seuil assez bas, pour éviter de supprimer 50% des données rentrées.
</pre>