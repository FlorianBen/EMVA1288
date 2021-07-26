from math import log10, log2, sqrt
import numpy as np
import matplotlib.pyplot as plt
import logging

import emva1288.common.processing as proc
import emva1288.common.input as inp
import emva1288.common.conversion as conv

DIR_OUT = 'run/out/'


def main():
    """ Main file for the EMVA1288 study.

    File 0 contains the dark images.
    File 1 to N contains the illumined images in ascending order in term of measured power.
    """
    # Variable à ajuster
    Nfile = 53  # Nombre de fichier de données hors dark
    res = np.zeros((Nfile, 7))  # Vecteur résultats
    fitd_sup = 70.0
    fitd_inf = 10

    logging.basicConfig(level=logging.INFO)

    # Information acquisition
    wavelenght = 530e-9  # Longueur d'onde de la LED
    roi = np.array([[255, 300], [1635, 945]])  # Zone d'étude
    bits = 12  # Nombre bits caméra
    index_im = np.array([4, 5])  # Index des images à utiliser

    # Chargement des données dark
    power_zero = np.abs(np.mean(inp.load_hdf5_attribute(
        inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(0).zfill(3) + '.h5', 'PowerWatt')))
    acq_time = np.mean(inp.load_hdf5_attribute(
        inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(0).zfill(3) + '.h5', 'AcquireTime'))
    # Conversion Puissance -> Ph/pix
    energy_zero = conv.photon_integration(power_zero, acq_time)
    nphoton_zero = conv.photon_total(energy_zero, wavelenght)
    nphoton_pm_zero = conv.area_sensor(nphoton_zero)
    nphoton_ppix_zero = nphoton_pm_zero * (5.85e-6*5.85e-6)
    # Chargement images dark
    data, _, _, _ = inp.load_hdf5(
        inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(0).zfill(3) + '.h5')
    # Prétraitement
    data = proc.scale(data, 16, bits)
    images = proc.roi_image(data[0:2], roi)
    # Calcul
    u_y_zero = proc.mean_grey_value(images)
    s_y_zero = proc.var_grey_value(images)

    # Initialise les graph
    fig1, ax1 = plt.subplots(figsize=[8.4, 4.8])
    fig2, ax2 = plt.subplots(figsize=[8.4, 4.8])
    fig3, ax3 = plt.subplots(figsize=[8.4, 4.8])
    fig4, ax4 = plt.subplots(figsize=[8.4, 4.8])
    fig5, ax5 = plt.subplots(figsize=[8.4, 4.8])

    # Boucle sur le signal
    for i in range(1, Nfile+1):
        ind = i - 1  # local index

        # Chargement des données dark
        power = np.abs(np.mean(inp.load_hdf5_attribute(
            inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(i).zfill(3) + '.h5', 'PowerWatt')))
        acq_time = np.mean(inp.load_hdf5_attribute(
            inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(i).zfill(3) + '.h5', 'AcquireTime'))
        # Conversion Puissance -> Ph/pix
        energy = conv.photon_integration(power, acq_time)
        nphoton = conv.photon_total(energy, wavelenght)
        nphoton_pm = conv.area_sensor(nphoton)
        nphoton_ppix = nphoton_pm * (5.85e-6*5.85e-6) - nphoton_ppix_zero
        # Print information
        logging.info('Image pair {} => {:3e} = {:3e}'.format(
            i, power, nphoton_ppix))
        # Chargement des images
        data, _, _, _ = inp.load_hdf5(
            inp.DATA_DIR + '2021_06_22/EMVA/cam1/' + '2021_06_22_EMVA_' + str(i).zfill(3) + '.h5')
        # Prétraitement
        data = proc.scale(data, 16, bits)
        images = proc.roi_image(data[index_im], roi)
        # Calcul de l'histogramme
        hist, bins = proc.hist_image(images, bits)
        # Calcul moyenne et variance
        u_y = proc.mean_grey_value(images)
        s_y = proc.var_grey_value(images)
        # Remplissement du vecteur résultats
        res[ind, 0] = i  # Indice
        res[ind, 1] = nphoton_ppix  # Nombre de photon/pixel
        res[ind, 2] = u_y  # Moyenne image
        res[ind, 3] = s_y  # Variance images
        res[ind, 4] = proc.mean_grey_value(
            images[0])-proc.mean_grey_value(images[1])  # Différence images
        res[ind, 5] = hist[-1]  # Pixels saturés
        res[ind, 6] = (u_y-u_y_zero)/np.sqrt(s_y)  # SNR

    # Fit courbe, determination de R
    popt1, pcov = proc.fit_curve(
        res[:, 1], res[:, 2] - u_y_zero, range=(fitd_inf, fitd_sup))
    R = popt1[1]
    # Fit courbe de transfer, determination de K
    popt2, pcov = proc.fit_curve(
        res[:, 2] - u_y_zero, res[:, 3] - s_y_zero, range=(fitd_inf, fitd_sup))
    K = popt2[1]
    # Calcul QE
    QE = R/K

    # Calcul des bruits
    sigmaq = 1.0/12.0  # Bruit electronique ????
    sigmad = np.sqrt(s_y_zero - sigmaq**2)/K

    # Calcul de la saturation
    ind_sat = np.argmax(res[:, 5] > images.size*0.002)  # - 1
    up_sat = res[ind_sat, 1]

    # Calcul du SNR évalué
    photons = np.logspace(-1, log10(up_sat), 200)
    snr2 = QE*photons/np.sqrt(sigmad**2+(sigmaq/K)**2+QE*photons)

    # Calcul du minimum de détecteur
    ind_min = np.argmax(snr2 > 1)
    up_min = photons[ind_min]

    # Print info
    logging.info('QE: {} %'.format(QE))
    logging.info('Gain: {} %'.format(K))
    logging.info('up.sat: {} ph'.format(up_sat))
    logging.info('up.min: {} ph'.format(up_min))
    logging.info('ue.sat: {} e-'.format(up_sat*QE))
    logging.info('ue.min: {} e-'.format(up_min*QE))
    logging.info('SNRmax {} dB'.format(20*log10(sqrt(up_sat*QE))))
    logging.info('DR: {} dB'.format(20*log10(up_sat/up_min)))
    logging.info('DR: {} bits'.format(log2(up_sat/up_min)))
    logging.info('sigd: {} e-'.format(sigmad))

    # Plotting section

    # Sensibilité
    xn_fit = np.linspace(np.min(res[:, 1]),
                         np.max(res[:, 1]), 100)
    ax1.plot(res[:, 1], res[:, 2] - u_y_zero, 'x', label='Data')
    ax1.plot(xn_fit, proc.fun_lin(xn_fit, *popt1),
             label='Fit: ${:.3f} \cdot x + {:.3f}$'.format(popt1[1], popt1[0]))
    ax1.set_title('Sensibility R')
    ax1.set_xlabel('$\mu_{p}$ ($\mathrm{{photons/pixel}}$)')
    ax1.set_ylabel('$\mu_{y} - \mu_{y.dark}$ ($\mathrm{{DN}}$)')
    ax1.grid()
    ax1.legend()
    fig1.savefig(DIR_OUT + 'fig_sensibilite.png')

    # Photon transfer
    xu_fit = np.linspace(np.min(res[:, 2] - u_y_zero),
                         np.max(res[:, 2] - u_y_zero), 100)
    ax2.plot(res[:, 2] - u_y_zero, res[:, 3] - s_y_zero, 'x', label='Data')
    ax2.plot(xu_fit, proc.fun_lin(xu_fit, *popt2),
             label='Fit: ${:.3f} \cdot x + {:.3f}$'.format(popt2[1], popt2[0]))
    ax2.set_title('Photon transfer K')
    ax2.set_xlabel('$\mu_{y} - \mu_{y.dark}$ ($\mathrm{{DN}}$)')
    ax2.set_ylabel('$\sigma^{2}_{y}$ ($\mathrm{{DN^{2}}}$)')
    ax2.grid()
    ax2.legend()
    fig2.savefig(DIR_OUT + 'fig_photon_transfert.png')

    # Stabilité
    ax3.plot(res[:, 2], res[:, 4], 'x', label='Difference between images')
    ax3.plot(res[:, 2], np.sqrt(res[:, 3]), label='STD images')
    ax3.set_title('Stability')
    ax3.set_xlabel('$\mu_{y}$ ($\mathrm{{DN}}$)')
    ax3.set_ylabel('$\sigma_{y}$ ($\mathrm{{DN}}$)')
    ax3.grid()
    ax3.legend()
    fig3.savefig(DIR_OUT + 'fig_stabilite.png')

    # Pixel saturés
    ax4.semilogy(res[:, 2], res[:, 5], 'x', label='Pixel overflow')
    ax4.axhline(images.size*0.002, color='r', label='Level EMVA')
    ax4.set_title('Pixel overflow')
    ax4.set_xlabel('$\mu_{y}$ ($\mathrm{{DN}}$)')
    ax4.set_ylabel('Overflow ($\mathrm{{pixels}}$)')
    ax4.grid()
    ax4.legend()
    fig4.savefig(DIR_OUT + 'fig_overflow.png')

    # SNR
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
