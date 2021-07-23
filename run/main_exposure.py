from scipy.ndimage.measurements import label
import yaml
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging

import emva1288.common.processing as proc
import emva1288.common.input as inp
import emva1288.common.conversion as conv

DIR_OUT = 'run/out/'


def main():
    """Mesure de
    """
    size = [13, 13, 13, 13, 13, 13]
    gain = [0, 7, 15, 20, 25, 30]
    dir = ['/Gain_000/2021_06_09_exposuretime0_',
           '/Gain_007/2021_06_09_exposuretime7_',
           '/Gain_015/2021_06_09_exposuretime15_',
           '/Gain_020/2021_06_09_exposuretime20_',
           '/Gain_025/2021_06_09_exposuretime25_',
           '/Gain_030/2021_06_09_exposuretime30_']
    index_im = np.array([0, 1])
    bits = 10

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for ind, name in enumerate(dir):
        res = np.zeros((size[ind], 4))
        for i in range(size[ind]):
            data, _, _, _ = inp.load_hdf5(
                inp.DATA_DIR + '2021_06_09/Exposure/' + name + str(i).zfill(3) + '.h5')
            offset = inp.load_hdf5_attribute(
                inp.DATA_DIR + '2021_06_09/Exposure/' + name + str(i).zfill(3) + '.h5', 'AcquireTime')

            images = proc.scale(data[index_im], 16, bits)

            u_y = proc.mean_grey_value(images)
            s_y = proc.var_grey_value(images)

            res[i, 0] = ind
            res[i, 1] = np.mean(offset[index_im])
            res[i, 2] = u_y
            res[i, 3] = s_y

        ax1.plot(res[:, 1], res[:, 2], '-x',
                 label='Gain {} $\mathrm{{dB}}$'.format(gain[ind]))
        ax2.plot(res[:, 1], res[:, 3], '-x',
                 label='Gain {} $\mathrm{{dB}}$'.format(gain[ind]))

    ax1.set_title(
        'Evolution $\mu_{y}$ en fonction du temps d\'exposition pour plusieur gain')
    ax1.set_xlabel('Temps d\'exposition ($\mathrm{{s}}$)')
    ax1.set_ylabel('Signal numérique moyen $\mu_{y}$ ($\mathrm{{DN}}$)')
    ax1.grid()
    ax1.legend()
    fig1.savefig(DIR_OUT + 'fig_mean_dark_t_gain.png')

    ax2.set_title(
        'Evolution $\sigma^{2}_{y}$ en fonction du temps d\'exposition pour plusieur gain')
    ax2.set_xlabel('Temps d\'exposition ($\mathrm{{s}}$)')
    ax2.set_ylabel('Signal numérique moyen $\sigma^{2}_{y}$ ($\mathrm{{DN}}$)')
    ax2.grid()
    ax2.legend()
    fig2.savefig(DIR_OUT + 'fig_sigma_dark_t_gain.png')

    # plt.show()


if __name__ == "__main__":
    # execute only if run as a script
    main()
