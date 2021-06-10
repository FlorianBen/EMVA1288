import yaml
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging

import emva1288.common.processing as proc
import emva1288.common.input as inp
import emva1288.common.conversion as conv


def main():
    """Mesure de
    """
    size = [13, 13, 13, 13, 13, 13]
    dir = ['/Gain_000/2021_06_09_exposuretime0_',
           '/Gain_007/2021_06_09_exposuretime7_',
           '/Gain_015/2021_06_09_exposuretime15_',
           '/Gain_020/2021_06_09_exposuretime20_',
           '/Gain_025/2021_06_09_exposuretime25_',
           '/Gain_030/2021_06_09_exposuretime30_']
    index_im = np.array([0, 1])
    bits = 10

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

        plt.plot(res[:, 1], res[:, 2], '-x')

    plt.show()


if __name__ == "__main__":
    # execute only if run as a script
    main()
