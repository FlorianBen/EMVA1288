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

    for ind, name in enumerate(dir):
        res = np.zeros((size[ind], 4))
        for i in range(size[ind]):
            data, _, _, _ = inp.load_hdf5(
                inp.DATA_DIR + '2021_06_08/Exposure/' + name + '2021_06_08_exposure_' + str(i).zfill(3) + '.h5')
            offset = inp.load_hdf5_attribute(
                inp.DATA_DIR + '2021_06_08/Exposure/' + name + '2021_06_08_exposure_' + str(i).zfill(3) + '.h5', 'AcquireTime')

            images = proc.scale(data[index_im], 16, bits)

            u_y = proc.mean_grey_value(images)
            s_y = proc.var_grey_value(images)

            res[i, 0] = ind
            res[i, 1] = np.mean(offset[index_im])
            res[i, 2] = u_y
            res[i, 3] = s_y

        plt.semilogx(res[:, 1], res[:, 3],'-x')

    plt.show()

if __name__ == "__main__":
    # execute only if run as a script
    main()