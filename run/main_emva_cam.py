from math import log10, log2, sqrt
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
    res = np.zeros((53, 7))

    # Info d'acquisition
    wavelenght = 530e-9
    roi = np.array([[255, 300], [1635, 945]])
    bits = 12
    index_im = np.array([4, 5])

    # Data dark
    power_zero = np.abs(np.mean(inp.load_hdf5_attribute(
        inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(0).zfill(3) + '.h5', 'PowerWatt')))
    acq_time = np.mean(inp.load_hdf5_attribute(
        inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(0).zfill(3) + '.h5', 'AcquireTime'))
    energy_zero = conv.photon_integration(power_zero, acq_time)
    nphoton_zero = conv.photon_total(energy_zero, wavelenght)
    nphoton_pm_zero = conv.area_sensor(nphoton_zero)
    nphoton_ppix_zero = nphoton_pm_zero * (5.85e-6*5.85e-6)
    data, _, _, _ = inp.load_hdf5(
        inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(0).zfill(3) + '.h5')
    data = proc.scale(data, 16, bits)
    images = proc.roi_image(data[0:2], roi)
    u_y_zero = proc.mean_grey_value(images)
    s_y_zero = proc.var_grey_value(images)

    fig1, ax1 = plt.subplots(figsize=[8.4,4.8])
    fig2, ax2 = plt.subplots(figsize=[8.4,4.8])
    fig3, ax3 = plt.subplots(figsize=[8.4,4.8])
    fig4, ax4 = plt.subplots(figsize=[8.4,4.8])
    fig5, ax5 = plt.subplots(figsize=[8.4,4.8])

    # Boucle sur le signal
    for i in range(1, 54):
        ind = i - 1

        power = np.abs(np.mean(inp.load_hdf5_attribute(
            inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(i).zfill(3) + '.h5', 'PowerWatt')))
        acq_time = np.mean(inp.load_hdf5_attribute(
            inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(i).zfill(3) + '.h5', 'AcquireTime'))
        energy = conv.photon_integration(power, acq_time)
        nphoton = conv.photon_total(energy, wavelenght)
        nphoton_pm = conv.area_sensor(nphoton)
        nphoton_ppix = nphoton_pm * (5.85e-6*5.85e-6) - nphoton_ppix_zero
        print('{} = {}'.format(i, nphoton_ppix))

        data, _, _, _ = inp.load_hdf5(
            inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(i).zfill(3) + '.h5')
        data = proc.scale(data, 16, bits)
        images = proc.roi_image(data[index_im], roi)

        hist, bins = proc.hist_image(images, bits)

        # print(proc.check_uniformity(images))

        # plt.step(bins[0:-1], hist, where='post')
        # plt.show()

        u_y = proc.mean_grey_value(images)
        s_y = proc.var_grey_value(images)

        res[ind, 0] = i  # Indice
        res[ind, 1] = nphoton_ppix  # Nombre de photon/pixel
        res[ind, 2] = u_y  # Moyenne image
        res[ind, 3] = s_y
        res[ind, 4] = proc.mean_grey_value(
            images[0])-proc.mean_grey_value(images[1])
        res[ind, 5] = hist[-1]
        res[ind, 6] = (u_y-u_y_zero)/np.sqrt(s_y)

    popt1, pcov = proc.fit_curve(
        res[:, 1], res[:, 2] - u_y_zero, range=(0, 65.8))

    popt2, pcov = proc.fit_curve(
        res[:, 2] - u_y_zero, res[:, 3] - s_y_zero, range=(0, 65.8))

    xn_fit = np.linspace(np.min(res[:, 1]),
                         np.max(res[:, 1]), 100)
    xu_fit = np.linspace(np.min(res[:, 2] - u_y_zero),
                         np.max(res[:, 2] - u_y_zero), 100)
    R = popt1[1]
    K = popt2[1]

    QE = R/K
    sigmaq = 1.0/12.0
    sigmad = np.sqrt(s_y_zero - sigmaq**2)/K

    ind_sat = np.argmax(res[:, 5] > images.size*0.002)  # - 1
    up_sat = res[ind_sat, 1]
    up_min = 1 * QE * (np.sqrt((s_y_zero/K)**2+1/4)+1/2)

    photons = np.logspace(-1, log10(up_sat), 200)
    snr2 = QE*photons/np.sqrt(sigmad**2+(sigmaq/K)**2+QE*photons)

    ind_min = np.argmax(snr2 > 1)
    up_min = photons[ind_min]

    # Print info
    print('QE: {} %'.format(QE))
    print('Gain: {} %'.format(K))
    print('up.sat: {} ph'.format(up_sat))
    print('up.min: {} ph'.format(up_min))
    print('ue.sat: {} e-'.format(up_sat*QE))
    print('ue.min: {} e-'.format(up_min*QE))
    print('SNRmax {} dB'.format(20*log10(sqrt(up_sat*QE))))
    print('DR: {} dB'.format(20*log10(up_sat/up_min)))
    print('DR: {} bits'.format(log2(up_sat/up_min)))
    print('sigd: {} e-'.format(sigmad))

    ax1.plot(res[:, 1], res[:, 2] - u_y_zero, 'x', label='Data')
    ax1.plot(xn_fit, proc.fun_lin(xn_fit, *popt1),
             label='Fit: ${:.3f} \cdot x + {:.3f}$'.format(popt1[1], popt1[0]))
    ax1.set_title('Sensibility R')
    ax1.set_xlabel('$\mu_{p}$ ($\mathrm{{photons/pixel}}$)')
    ax1.set_ylabel('$\mu_{y} - \mu_{y.dark}$ ($\mathrm{{DN}}$)')
    ax1.grid()
    ax1.legend()
    fig1.savefig(DIR_OUT + 'fig_sensibilite.png')

    ax2.plot(res[:, 2] - u_y_zero, res[:, 3] - s_y_zero, 'x', label='Data')
    ax2.plot(xu_fit, proc.fun_lin(xu_fit, *popt2),
             label='Fit: ${:.3f} \cdot x + {:.3f}$'.format(popt2[1], popt2[0]))
    ax2.set_title('Photon transfer K')
    ax2.set_xlabel('$\mu_{y} - \mu_{y.dark}$ ($\mathrm{{DN}}$)')
    ax2.set_ylabel('$\sigma^{2}_{y}$ ($\mathrm{{DN^{2}}}$)')
    ax2.grid()
    ax2.legend()
    fig2.savefig(DIR_OUT + 'fig_photon_transfert.png')

    ax3.plot(res[:, 2], res[:, 4], 'x', label='Difference between images')
    ax3.plot(res[:, 2], np.sqrt(res[:, 3]), label='STD images')
    ax3.set_title('Stability')
    ax3.set_xlabel('$\mu_{y}$ ($\mathrm{{DN}}$)')
    ax3.set_ylabel('$\sigma_{y}$ ($\mathrm{{DN}}$)')
    ax3.grid()
    ax3.legend()
    fig3.savefig(DIR_OUT + 'fig_stabilite.png')

    ax4.semilogy(res[:, 2], res[:, 5], 'x', label='Pixel overflow')
    ax4.axhline(images.size*0.002, color='r', label='Level EMVA')
    ax4.set_title('Pixel overflow')
    ax4.set_xlabel('$\mu_{y}$ ($\mathrm{{DN}}$)')
    ax4.set_ylabel('Overflow ($\mathrm{{pixels}}$)')
    ax4.grid()
    ax4.legend()
    fig4.savefig(DIR_OUT + 'fig_overflow.png')

    pixth = np.logspace(0, 6, 100)
    ax5.loglog(res[:, 1], res[:, 6], 'x', label='SNR measured')
    ax5.loglog(pixth, np.sqrt(pixth), color='g', label='SNR ideal sensor')
    ax5.loglog(photons, snr2, '-', label='SNR evaluated')
    ax5.axvline(up_min, ls=':', color='b', label='$\mu_{p.min}$')
    ax5.axvline(up_sat, ls=':', color='r', label='$\mu_{p.sat}$')
    ax5.set_xlim(1, 10**6)
    ax5.set_ylim(10**-1, 10**3)
    ax5.set_title('SNR')
    ax5.set_xlabel('$\mu_{p}$ ($\mathrm{{DN}}$)')
    ax5.set_xlabel('$\mu_{p}$ ($\mathrm{{photons/pixel}}$)')
    ax5.grid(which='both')
    ax5.legend()
    fig5.savefig(DIR_OUT + 'fig_snr.png')

    plt.show()


if __name__ == "__main__":
    # execute only if run as a script
    main()
