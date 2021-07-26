import h5py
import numpy as np
import logging
import sys

DATA_DIR = '/local/home/fb250757/Documents/Data/Calibration2/'


def load_hdf5(filename):
    """Load data images from an HDF5 file.

    Args:
        filename (string): Full path of the HDF5 file.

    Returns:
        (ndarray): Images data.
    """
    try:
        file = h5py.File(filename, 'r')
        data = file['entry/data/data'][:]
        timestamp = file['entry/instrument/NDAttributes/NDArrayTimeStamp'][:]
        time_s = file['entry/instrument/NDAttributes/NDArrayEpicsTSSec'][:]
        time_ns = file['entry/instrument/NDAttributes/NDArrayEpicsTSnSec'][:]
        file.close()
        return data, timestamp, time_s, time_ns
    except (OSError):
        logging.exception('Unable to open file')
        sys.exit(1)


def load_hdf5_attribute(filename, attribute_name):
    try:
        file = h5py.File(filename, 'r')
        attribute = file['entry/instrument/NDAttributes/' + attribute_name][:]
        file.close()
        return attribute
    except (OSError):
        logging.exception('Unable to open file')
        sys.exit(1)


def load_png(filename):
    """Load data image from a PNG image.

    Args:
        filename (string): Full path of the image.

    Returns:
        (ndarray): Image data.
    """
    try:
        logging.info('Trying to open a PNG file {}'.format(filename))
        image = np.zeros((10, 10))
        return image
    except (OSError):
        logging.exception('Unable to open file')
        sys.exit(1)


def load_bpm(filename):
    """Load data image from a BPM image.

    Args:
        filename (string): Full path of the image.

    Returns:
        (ndarray): Image data.
    """
    try:
        logging.info('Try to open an BPM file {}'.format(filename))
        image = np.zeros((10, 10))
        return image
    except (OSError):
        logging.exception('Unable to open file')
        sys.exit(1)
    pass
