import h5py
import numpy as np
import logging
import sys

DATA_DIR = '/local/home/fb250757/Documents/Data/Calibration/'


def load_hdf5(filename):
    """Load data images from an HDF5 file.

    Args:
        filename (string): Full path of the HDF5 file.

    Returns:
        (ndarray): Images data.
    """
    try:
        logging.info('Try to open file {}'.format(filename))
        file = h5py.File(filename, 'r')
        logging.info('File open: done')
        data = file['detector/data1'][:]
        timestamp = 0#file['entry/instrument/NDAttributes/NDArrayTimeStamp'][:]
        time_s = 0#file['entry/instrument/NDAttributes/NDArrayEpicsTSSec'][:]
        time_ns = 0#file['entry/instrument/NDAttributes/NDArrayEpicsTSnSec'][:]
        logging.info('Read data: done')
        file.close()
        logging.info('File is close '.format(filename))
        return data, timestamp, time_s, time_ns
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
