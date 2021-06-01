import numpy as np

sol = 299792458
hplanck = 6.62607015e-34
e_coulomb = 1.602176634e-19

def photon_total(energy, wavelenght):
    return energy/photon_J(wavelenght)


def photon_integration(W, t):
    return W*t


def area_sensor(val, diameter=0.0095):
    sensor_surf = 2 * np.pi * diameter/2
    return val/sensor_surf


def JtoeV(joule):
    return joule/e_coulomb


def eVtoJ(eV):
    return eV*e_coulomb


def photon_J(wavelenght):
    return (sol*hplanck)/wavelenght