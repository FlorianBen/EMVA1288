import numpy as np


def mean_grey_value(images):
    """Compute the mean grey value of at least two images

    Args:
        images (ndarray): Input images, two images should be provided.
    Returns:
        float : Mean of the grey value.
    """
    imean = np.mean(images, axis=0)
    pix_mean = np.mean(imean)
    return pix_mean


def var_grey_value(images):
    """Compute the temporal variance of grey value.

    Args:
        images (ndarray): Input images, two images should be provided.

    Returns:
        float : Temporal variance of the grey value.
    """
    temp = (images[0]-images[1])**2 - 0.5 * \
        (np.mean(images[0])-np.mean(images[1]))**2
    pix_var = np.sum(temp)/np.size(images)
    return pix_var


def compute_snr(images, dark):
    """Compute the Signal to Noise ratio of an image.

    Args:
        images (ndarray): Input images, two images sould be provided.
        dark (ndarray): Dark frames, two images should be provided.

    Returns:
        float: Signal to Noise ratio
    """
    snr = (mean_grey_value(images)-mean_grey_value(dark)) / \
        var_grey_value(images)
    return snr