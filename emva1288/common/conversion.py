import numpy as np

sol = 299792458
hplanck = 6.62607015e-34
e_coulomb = 1.602176634e-19

def photon_total(energy, wavelenght):
    """Compute the total number of photons according to the wavelenght.

    Args:
        energy (float): Measure energy.
        wavelenght (float): Wavelenght of the photons.

    Returns:
        float: Total number of photons.
    """
    return energy/photon_J(wavelenght)


def photon_integration(W, t):
    """Compute the energy according to the power and the integration time.

    Args:
        W (float): Power in W.
        t (float): Integration time in second.

    Returns:
        float: Energy.
    """
    return W*t


def area_sensor(val, diameter=0.0095):
    """Normalize the value according to the sensor surface.

    Args:
        val (float): Value to normalize.
        diameter (float, optional): Sensor diameter. Defaults to 0.0095.

    Returns:
        float: Normalized value.
    """
    sensor_surf = np.pi * (diameter/2)**2
    return val/sensor_surf


def JtoeV(joule):
    """Convert Joule to electronvolt.

    Args:
        joule (float): Value to convert.

    Returns:
        float: Converted value.
    """
    return joule/e_coulomb


def eVtoJ(eV):
    """Convert electronvolt to Joule.

    Args:
        eV (float): Value to convert.

    Returns:
        float: Converted value.
    """
    return eV*e_coulomb


def photon_J(wavelenght):
    """Convert photon energy in to nanometer to photon energy in Joule.

    Args:
        wavelenght (float): Photon wavelenght.

    Returns:
        float: Photon energy in Joule.
    """
    return (sol*hplanck)/wavelenght