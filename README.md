# Calibration des caméra ESS avec le standard EMVA 1288

## Introduction

L'IRFU, dans le cadre du projet ESS NPM, doit livrer 10 détecteurs type IPM utilisant des MCP.
Avant la livraison à ESS, chaque MCP est vérifié en traçant une courbe de gain. 
Une fois arrivé le MCP est retesté pour vérifier son bon fonctionnement.
Sans calibration des caméras, les courbes de gain sont exprimées en unité arbitraire. 
L'objectif de la calibration des caméras est de pouvoir donner une courbe de gain la plus absolue possible.
La calibration se fera suivant le standard EMVA 1288 car celui-ci reste simple et accessible.
## EMVA 1288

## Setup
### Calibration

Le montage de calibration n'est pas optimal mais il est simple et peu onéreux.
Une LED, de la même longueur d'onde que le MCP, irradie un diffuseur pseudo uniforme et une lentille collimate le faisceau en sortie.
À l'aide d'un cube séparateur, on envoie la lumière de la LED à la fois sur la caméra à tester et sur un puissance-mètre. 
La puissance sur le capteur est donc connue. 
Avec plusieurs paramètres de caméra et d'intensité de LED, on peut caractériser le capteur de la caméra.
Avant de faire les mesures de calibration, chaque élément optique est soigneusement caractérisé à l'aide du puissance-mètre.

## Résultats