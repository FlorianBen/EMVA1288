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

La liste du matériel achetable chez Thorlabs est disponible ci dessous :

| Item                           | Ref          | Prix unitaire (€) | Quantité |
| ------------------------------ | ------------ | ----------------- | -------- |
| LED 530 nm                     | M530L4       | 269.52            | 1        |
| LED Driver                     | LEDD1B       | 294.11            | 1        |
| Coupleur SM1                   | SM1T2        | 19.58             | 1        |
| Cage 30 mm                     | CP33/M       | 15.35             | 3        |
| Cage 30 mm 1”                  | CP35/M       | 16.98             | 2        |
| Diffuser grit 220              | DG10-220     | 14.66             | 1        |
| Diffuser grit 1500             | DG10-1500    | 14.66             | 1        |
| Plano-Convex Lens 30 mm        | LA1805       | 22.38             | 1        |
| Plano-Convex Lens 60 mm        | LA1134       | 20.63             | 1        |
| Plano-Convex Lens 100 mm       | LA1509       | 19.77             | 1        |
| Cage Cube-Mounted Beamsplitter | CCM1-BS013/M | 259.52            | 1        |
| Sliding Filter Mount Bundle    | CFS1ND/M     | 265.58            | 1        |
| Adapter C-Mount/SM1            | SM1A39       | 19.28             | 1        |
| Photodiode Power Sensors       | S120C        | 295.1             | 1        |
| Power Meter Interface          | PM101A       | 430.68            | 1        |
| Rod 6” engraved                | ER6E         | 15.64             | 3        |
| Rod 6” pack of 4               | ER6-P4       | 30.78             | 3        |
| Cage Plate Stops for ER Rods   | ERCPS        | 40.58             | 3        |
| Cage System Covers             | C30L24       | 27.27             | 1        |

## Résultats