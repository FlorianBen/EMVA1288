# Calibration des caméras ESS avec le standard EMVA 1288

## Introduction

L'IRFU, dans le cadre du projet ESS NPM, doit livrer 10 détecteurs type IPM utilisant des MCP.
Avant la livraison à ESS, chaque MCP est vérifié en traçant une courbe de gain. 
Une fois arrivé le MCP est retesté pour vérifier son bon fonctionnement.
Sans calibration des caméras, les courbes de gain sont exprimées en unité arbitraire. 
L'objectif de la calibration des caméras est de pouvoir donner une courbe de gain la plus absolue possible.
La calibration se fera suivant le standard EMVA 1288 car celui-ci reste simple et accessible.
## EMVA 1288

## Setup
### Camera

La caméra utilisée est la Blackfly BFLY-PGE-23S6M de chez FLIR (anciennement Point Grey).
Elle est basée sur le capteur CMOS IMX249 de chez Sony, dont les caractéristiques générales sont données dans le tableau suivant :
| Property             | Value                      |
| -------------------- | -------------------------- |
| Resolution           | 1936 (H)\,\times\,1216 (V) |
| Pixel size           | 5.86 $\mu m$               |
| Sensor diagonal size | 13.4 mm (Type 1/1.2)       |
| Well capacity        | 32000 $e^-$-               |
| Dynamic Range        | 70 dB                      |
| QE at 525 nm         | 70 \%                      |
| Electrons noise      | 6.8 $e^-$                  |
| ADC                  | 8, 10 or 12 bits           |
| Max frame rate       | 30 fps                     |

On souhaite vérifier et avoir des caractéristiques réaliste du capteur.

La caméra est pilotable via un support EPICS, voir [ici](resources/epics/README.md).

### Calibration

Le montage de calibration n'est pas optimal mais il est simple et peu onéreux.
Une LED, de la même longueur d'onde que le MCP, irradie un diffuseur pseudo uniforme et une lentille collimate le faisceau en sortie.
À l'aide d'un cube séparateur, on envoie la lumière de la LED à la fois sur la caméra à tester et sur un puissance-mètre. 
La puissance sur le capteur est donc connue. 
Avec plusieurs paramètres de caméra et d'intensité de LED, on peut caractériser le capteur de la caméra.
Avant de faire les mesures de calibration, chaque élément optique est soigneusement caractérisé à l'aide du puissance-mètre.

## Résultats