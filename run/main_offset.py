import yaml
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging

import emva1288.common.processing as proc
import emva1288.common.input as inp
import emva1288.common.conversion as conv

def main():
    size = [28, 16]
    dir = ['/Offset1/', '/Offset2/']

    for ind, name in enumerate(dir):
        res = np.zeros((size[ind], 2))
        for i in range(size[ind]):
            data, _, _, _ = inp.load_hdf5(
                inp.DATA_DIR + '2021_06_07/' + name + '2021_06_07_offset_' + str(i).zfill(3) + '.h5')
            offset = inp.load_hdf5_attribute(
                inp.DATA_DIR + '2021_06_07/' + name + '2021_06_07_offset_' + str(i).zfill(3) + '.h5', 'Offset')

            bits = 10
            image = proc.scale(data[9], 16, bits)
            hist, bins = proc.hist_image(image, bits)
            res[i, 0] = offset[0]
            res[i, 1] = hist[0]
            #plt.step(bins[0:-1], hist, where='post')    
            #plt.show()


        res = res[res[:, 0].argsort()]
        plt.semilogy(res[:, 0], res[:, 1],'-x')
    
    plt.axhline(image.size*0.005)
    plt.show()

if __name__ == "__main__":
    # execute only if run as a script
    main()