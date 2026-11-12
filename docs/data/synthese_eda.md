# Synthèse de l'analyse exploratoire (EDA)

> Détail, graphiques et code : [`notebooks/eda_reference.ipynb`](../../notebooks/eda_reference.ipynb).
> Source : Open Food Facts, licence ODbL. Données nettoyées par `src/cleaning.prepare_data`.

## Le périmètre en 3 chiffres

| | |
|---|---|
| Produits vendus en France, après nettoyage | **456 479** |
| Rayons (groupes alimentaires de niveau 1) | **9** |
| Produits avec un Nutri-Score A à E | **92,4 %** (contre 37,2 % sur toute la France) |

## Les 5 messages

1. **Deux rayons pèsent 39 % du périmètre.** Les snacks sucrés (21,6 %) et la viande-poisson-œufs dominent : une moyenne « tous rayons » reflète surtout ces deux-là.
2. **Le Nutri-Score dépend d'abord du rayon.** 60 % des fruits et légumes sont notés A ou B, contre 2 % des snacks sucrés (dont 93 % sont D ou E).
3. **Seules les fibres manquent vraiment.** Elles sont absentes dans 29,5 % à 62,3 % des produits selon le rayon ; les 7 nutriments obligatoires manquent dans 7,0 % des produits au plus.
4. **Aucun nutriment ne suffit seul, sauf au sein d'un rayon.** Sur tout le périmètre, le lien avec le Nutri-Score ne dépasse pas 0,48 (énergie, graisses saturées). Dans un rayon, il monte à 0,80 (le sel pour la viande-poisson-œufs) et 0,75 (le sucre pour les boissons).
5. **846 produits incohérents ont passé le nettoyage** (0,19 %), dont 224 snacks sucrés : sucres supérieurs aux glucides, plus de 105 g de nutriments pour 100 g, ou 0 kcal avec des graisses. Les valeurs extrêmes restantes sont, elles, réelles (3 051 miels à 79,8 g de sucre en médiane).

## Ce que ça change pour la suite

- **Comparer les produits au sein d'un rayon**, jamais sur tout le périmètre : une substitution vise le « mieux relatif » (un snack sucré C plutôt que E).
- **Le rayon est une variable clé du futur modèle**, à combiner avec les nutriments.
- **Ne pas s'appuyer sur les fibres** sans traiter leurs manquants : les écarter, ou les compléter avec prudence.
- **Ajouter un drapeau de fiabilité** sur les 846 produits incohérents, plutôt que de les supprimer.

## Limites

- Les valeurs sont déclarées par des contributeurs, pas mesurées en laboratoire.
- Le périmètre ne garde que les produits ayant un nom et une énergie : il est plus complet que la base France, donc pas représentatif de tout ce qui est en rayon.
