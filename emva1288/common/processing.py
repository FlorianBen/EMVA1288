from matplotlib.colors import cnames
import numpy as np
from scipy.ndimage import convolve


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


def temporal_variance(images):
    """Compute the temporal variance image from several images.

    Args:
        images (ndarray): Input images (3D data).

    Returns:
        ndarray: Temporal variance images.
    """
    if images.ndim == 3:
        return np.var(images, axis=0, ddof=1)
    else:
        raise TypeError("The input should be a 3D array")


def spatial_variance(images):
    """Compute the spatial variance from one or several images.

    Args:
        images (ndarray): Input image or images.

    Returns:
        float or ndarray: Spatial variance.
    """
    if images.ndim == 3:
        return np.var(images, axis=(1, 2))
    elif images.ndim == 2:
        return np.var(images)
    else:
        raise TypeError("The input should be a 2D or 3D array")


def B3spline(x):
    """Compute B-Spline function defined in the EMVA 1288 standard.

    Args:
        x (float or ndarray): Input value.

    Returns:
        float or ndarray: Function value at the input value.
    """
    return np.where(abs(x) < 1, 2.0/3.0-abs(x)**2 + 1.0/2.0*abs(x)**2, 0) + \
        np.where(np.logical_and(1 <= abs(x), abs(x) <= 2),
                 1.0/6.0*(2.0-abs(x))**3, 0)


def hist_image(image, nbits):
    """Compute the histogram for the given image.

    Args:
        image (ndarry): Input image
        nbits (int): Deepth of pixel in bit.

    Returns:
        tuple: histogram values and bins
    """
    bins = np.linspace(0, 2**nbits-1, 2**nbits)
    valbins, _ = np.histogram(image, bins)
    return valbins, bins


def box_filter(image, size):
    """Apply box filter to an image.

    Args:
        image (ndarray): Input image.
        size (int): Dimension of the filter.

    Returns:
        ndarray: Filtered image.
    """
    filter = np.ones((size, size))
    filter = filter/filter.size
    out = convolve(image, filter)
    return out


def binomial_filter(image, dim):
    """Apply binomial filter to an image.

    Args:
        image (ndarray): Input image to filter.
        dim (int): Filter dimension.
    """
    base = np.array([1, 1])
    prev = base
    dim_v = dim-2
    mat = np.zeros((dim, dim))
    for i in range(dim_v):
        prev = np.convolve(base, prev)
    mat[int(dim/2), :] = prev
    mat[:, int(dim/2)] = prev
    mat = mat/np.sum(mat)
    out = convolve(image, mat)
    return out

def scale(image, nbitsin, nbitsout):
    """Scale the image.

    Args:
        image (ndarray): Input image.
        nbitsin (int): Deepth of the input image in bits.
        nbitsout (int): Depth of the output image.

    Returns:
        ndarray: Output image.
    """
    scale = (2**nbitsin)/(2**nbitsout)
    out = image/scale
    return out