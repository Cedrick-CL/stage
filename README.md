# Traduction d'un programme logique produit par LFIT en automate asynchrone

## Table des matières
- [Description](#description)
- [Fonctionnement](#fonctionnement)
- [Utilisation](#utilisation)
- [Limites](#limite)

## Description
LFIT (Ribeiro et al., Machine Learning, 2021) est une méthode d'apprentissage automatique (machine learning) symbolique et explicable. À partir de traces d'exécution discrètes, elle produit un programme logique représentant exactement ces observations, permettant de retrouver la structure dynamique modulaire du système. Ce programme logique peut être utilisé pour reproduire les observations.

Il est connu que le programme logique est équivalent à un automate asynchrone (Folschette et al, CS2Bio, 2013). L'objectif de ce stage est d'implémenter cette traduction.

À l'issue de celui-ci, une traduction dans les formats Pint, Ginml, PyBoolnet et SBML-qaud a été réalisée.

## Fonctionnement

L'ensemble des fonctions de traduction sont dans le dossier `Format`.

Les quatres fonctions :

- `modelToPint(modele, outputFile)`
- `modelToGinml(modele, outputFile)`
- `modelToSbmlQual(modele, outputFile)`
- `modelToPyboolnet(modele, outputFile)`

prennent en argument un modèle, un programme logique issue de l'algorithme Dynamic multi‑valued logic program (DMVLP), ainsi qu'un fichier de sortie, dans lequel on trouvera la traduction du modèle dans le format souhaité.

