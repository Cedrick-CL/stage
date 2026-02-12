# Traduction d'un programme logique produit par LFIT en automate asynchrone

## Table des matières
- [Description](#description)
- [Utilisation](#utilisation)
- [Fonctionnement et limites](#fonctionnement-et-limites)

## Description
LFIT (Ribeiro et al., Machine Learning, 2021) est une méthode d'apprentissage automatique (machine learning) symbolique et explicable. À partir de traces d'exécution discrètes, elle produit un programme logique représentant exactement ces observations, permettant de retrouver la structure dynamique modulaire du système. Ce programme logique peut être utilisé pour reproduire les observations.

Il est connu que le programme logique est équivalent à un automate asynchrone (Folschette et al, CS2Bio, 2013). L'objectif de ce stage est d'implémenter cette traduction.

À l'issue de celui-ci, une traduction dans les formats Pint, Ginml, PyBoolnet et SBML-qaud a été réalisée.

## Utilisation

L'ensemble des fonctions de traduction sont dans le dossier `Format`.

Les quatres fonctions :

- `modelToPint(modele, outputFile)`
- `modelToGinml(modele, outputFile)`
- `modelToSbmlQual(modele, outputFile)`
- `modelToPyboolnet(modele, outputFile)`

prennent en argument un modèle, un programme logique issue de l'algorithme Dynamic multi‑valued logic program (DMVLP), ainsi qu'un fichier de sortie, dans lequel on trouvera la traduction du modèle dans le format souhaité.

## Fonctionnement et limites
Les quatre fonctions présentées ci‑dessus reposent sur le même principe :
- Extraction des règles et des variables utilisées dans le modèle.
- Écriture de l’automate asynchrone correspondant selon une syntaxe spécifique.

La procédure de récupération d’un modèle à partir de données expérimentales est décrite par Tony Ribeiro sur sa page GitHub consacrée à PyLfit.

Pour la suite, on prendra pour exemple les données suivantes, ainsi que le modèle associé.

```text
data = [ \
(["0","0","0"],["0","0","1"]), \
(["1","0","0"],["0","0","0"]), \
(["0","1","0"],["1","0","1"]), \
(["0","0","1"],["0","0","1"]), \
(["1","1","0"],["1","0","0"]), \
(["1","0","1"],["0","1","0"]), \
(["0","1","1"],["1","0","1"]), \
(["1","1","1"],["1","1","0"])]

dataset = pylfit.preprocessing.discrete_state_transitions_dataset_from_array(data=data, feature_names=["p_t_1","q_t_1","r_t_1"], target_names=["p_t","q_t","r_t"])

model = pylfit.models.DMVLP(features=dataset.features, targets=dataset.targets)
model.compile(algorithm="pride") 

model.fit(dataset=dataset)
```
### 1. Format Pint (`.an`)

Le format `.an` (Automata Networks) est utilisé par l'outil [Pint](https://loicpauleve.name/pint/doc/automata-networks.html). 

**Structure du fichier généré :**

* **Déclaration des variables :** Chaque variable est définie avec l'ensemble de ses états possibles.
    ```text
    "p" ["0", "1"]
    "q" ["0", "1"]
    "r" ["0", "1"]
    ```
* **Transitions :** Les règles logiques sont traduites selon la syntaxe :  
    `"variable" état_initial -> état_final when "condition"`

  Pour le modèle d'exemple, le fichier produit contient :

  ```text
  "p" "1" -> "0" when "q"="0"
  "p" "0" -> "1" when "q"="1"
  "q" "1" -> "0" when "r"="0"
  "q" "1" -> "0" when "p"="0"
  "q" "0" -> "1" when "p"="1" and "r"="1"
  "r" "1" -> "0" when "p"="1"
  "r" "0" -> "1" when "p"="0"
  ```
L'implémentation pour ce format supporte aussi bien les variables booléennes que multi-valuées.


