import yaml
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging

import emva1288.common.processing as proc
import emva1288.common.input as inp
import emva1288.common.conversion as conv


def main():
    size = [13, 13, 13]
    dir = ['/Gain_001/', '/Gain_002/', 'Gain_003/']
    index_im = np.array([0, 1])
    bits = 10

    data, _, _, _ = inp.load_hdf5(
        inp.DATA_DIR + '2021_06_08/Flat/' + '2021_06_08_flat_' + str(3).zfill(3) + '.h5')
    images = proc.scale(data, 16, bits)

    stack_dark = np.mean(images, axis=0)
    stack_dark_f = proc.emva_filter(stack_dark)

    data, _, _, _ = inp.load_hdf5(
        inp.DATA_DIR + '2021_06_08/Flat/' + '2021_06_08_flat_' + str(2).zfill(3) + '.h5')
    images = proc.scale(data, 16, bits)

    stack_half = np.mean(images, axis=0)
    stack_half_f = proc.emva_filter(stack_half)

    #plt.imshow(stack_dark_f, clim=(-1, 1))
    plt.plot(np.sum(stack_dark_f, axis=1))
    plt.show()


if __name__ == "__main__":
    # execute only if run as a script
    main()
