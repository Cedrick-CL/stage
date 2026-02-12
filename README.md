# Traduction d'un programme logique produit par LFIT en automate asynchrone

## Table des matières
- [Description](#description)
- [Organisation](#organisation)
- [Utilisation](#utilisation)
- [Fonctionnement et limites](#fonctionnement-et-limites)
- [Bibliographie](#bibliographie)

## Description
LFIT (Ribeiro et al., Machine Learning, 2021) est une méthode d'apprentissage automatique (machine learning) symbolique et explicable. À partir de traces d'exécution discrètes, elle produit un programme logique représentant exactement ces observations, permettant de retrouver la structure dynamique modulaire du système. Ce programme logique peut être utilisé pour reproduire les observations.

Il est connu que le programme logique est équivalent à un automate asynchrone (Folschette et al, CS2Bio, 2013). L'objectif de ce stage est d'implémenter cette traduction.

À l'issue de celui-ci, une traduction dans les formats Pint, Ginml, PyBoolnet et SBML-qaud a été réalisée.

## Organisation

Vous trouverez dans le dossier `Format` les différentes fonctions de traduction dans les différents formats décrits plus bas. 

Dans le dossier `Exemples`, différents applications des algorithmes et enfin un dernier fichier `readGraphe.py` qui gère la lecture des fichiers `.dot`.

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

### 2. Format Ginml (`.ginml`)

Ce format de traduction a posé plus de problèmes, notamment concernant la syntaxe des fichiers concernés. 

Pour éviter d'écrire des bêtises, je ne détaillerai pas plus ce qui a été fait. Si vous souhaitez voir les détails, le code est disponible dans le fichier `.py` associé dans le dossier `Format`, et des exemples de sorties sont trouvables dans le dossier `Exemples`. Il est tout à fait possible d'ouvrir le fichier de sorti avec Ginsim, mais des incompréhension persistent en ce qui concerne les conditions d'activation (les règles and notamment), ce qui fait qu'en sortie, on n'obtient pas tout à fait le même graphe (pour plus de détails, voir le notebook `rendu.ipynb`).

**Limites de l'implémentation :**
* L'algorithme de traduction n'est efficace que pour les variables **booléennes**. 
* Pour les variables **multi-valuées**, tout ce qui n'est pas un `0` est considéré comme un `1`.

### 3. Format PyBoolnet (`.bnet`)

En ce qui concerne ce format, on écrit tout simplement pour chaque variable la règle logique associée.

  Pour le modèle d'exemple, le fichier produit contient :

  ```text
p, q
q, (p & r)
r, !p
  ```

Ce type de fichier ne peut traiter que les variables booléenes, mais comme pour le format Ginml, pour les variables multi-valuées, tout ce qui n'est pas un `0` est considéré comme un `1`

### 4. Format SBML-quad (`.sbml`)

Ce dernier format s'appuie sur les formules logiques associées aux différentes variables.
L'algorithme de traduction dans ce format s'appuie donc sur l'algorithme utilsé pour le format PyBoolnet, et les différentes fonctions décrites dans la [documentation de SBML-quad]([https://loicpauleve.name/pint/doc/automata-networks.html](https://sbml.org/software/libsbml/5.18.0/docs/formatted/python-api/namespacelibsbml.html)) permet de générer éfficacement le fichier de sortie dans le format souhaité.

Il est possible de vérifier le fichier de sortie associé à notre exemple dans le dossier `Exemple/dataREADme`.

L'implémentation pour ce format supporte aussi bien les variables booléennes que multi-valuées.

## Bibliographie

### Logiciels et Bibliothèques
* **GINsim** : [Documentation officielle](https://ginsim.github.io/documentation/)
* **libSBML** : [Dépôt GitHub](https://github.com/sbmlteam/libsbml), [Page Wikipedia](https://en.wikipedia.org/wiki/LibSBML) et [Documentation API Python (SBasePlugin)](https://sbml.org/software/libsbml/5.18.0/docs/formatted/python-api/classlibsbml_1_1_s_base_plugin.html)
* **pylfit** : [Dépôt GitHub (Tony-sama)](https://github.com/Tony-sama/pylfit)

### Formats de fichiers
* **GINML** : [Spécifications du format](https://colomoto.github.io/formats/ginml/)
* **SBML-qual** : [Spécifications du format](https://colomoto.github.io/formats/sbml-qual/)
* **Pint** : [Spécifications du format](https://loicpauleve.name/pint/doc/automata-networks.html)

### Articles et Publications
* **Naldi, A., et al. (2010)**. *GINsim: a software suite for the modeling and simulation of gene regulatory networks*. Bioinformatics, 26(10), 1378–1379. [DOI: 10.1093/bioinformatics/btq129](https://academic.oup.com/bioinformatics/article/26/10/1378/193238)
* **Folschette, M., et al. (2015)**. *Inference of Boolean networks from time series of gene expression*. [PDF](http://maxime.folschette.fr/Folschette_TCS15.pdf)
* **Ribeiro, T., et al. (2021)**. *Learning Logic Programs for Modeling Gene Regulatory Networks*. [PDF](http://maxime.folschette.fr/Ribeiro_ML21.pdf)
* **Richard, A., Comet, J.-P., & Bernot, G. (2008)**. *Formal Methods for Modeling Biological Regulatory Networks*. [Notes de cours (Lille)](https://webusers.i3s.unice.fr/~bernot/Teaching/2008-LilleSchool-RichardCometBernot.pdf)
* **CHEVRON Guillaume, FIGUEIREDO BORRMANN Yuri, HAMILA Fatma, JUNG-MULLER Mathieu, SCHIEFFER Gabin (2021)**. *Vérification de propriétés dynamiques de modèles inférés par LFIT à l’aide de la bibliothèque CoLoMoTo*. [Rapport](2021.03.30–RapportfinalCoLoMoTov2-2.pdf)
