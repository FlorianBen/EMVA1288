import h5py
import numpy as np
import logging
import sys

DATA_DIR = '/local/home/fb250757/Documents/Data/Camera/'


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
        data = file['entry/data/data'][:]
        timestamp = file['entry/instrument/NDAttributes/NDArrayTimeStamp'][:]
        time_s = file['entry/instrument/NDAttributes/NDArrayEpicsTSSec'][:]
        time_ns = file['entry/instrument/NDAttributes/NDArrayEpicsTSnSec'][:]
        logging.info('Read data: done')
        file.close()
        logging.info('File is close '.format(filename))
        return data, timestamp, time_s, time_ns
    except (OSError):
        logging.exception('Unable to open file')
        sys.exit(1)

def load_png():
    pass

def load_bpm():
    pass