import logging
from matplotlib.colors import cnames
import numpy as np
from numpy import ma
from scipy.ndimage import convolve
from scipy import optimize


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


def roi_image(images, roi):
    """Select a Region of Interest (ROI) in the image.

    Args:
        images (ndarray): Input image.
        roi (ndarray): ROI coordinates ((x,y),(stepx,stepy)).

    Raises:
        TypeError: Incorrect image dimension.

    Returns:
        ndarray: Output ROI images.
    """
    if images.ndim == 3:
        return images[:, roi[0, 1]:roi[1, 1], roi[0, 0]:roi[1, 0]]
    elif images.ndim == 2:
        return images[roi[0, 1]:roi[1, 1], roi[0, 0]:roi[1, 0]]
    else:
        raise TypeError(
            'Input image must be a 2D image or 3D array of images !')


def check_uniformity(image, filtering=True):
    if filtering:
        image = box_filter(image, 3)
        image = box_filter(image, 7)

    max = np.max(image)
    min = np.min(image)
    mean = np.mean(image)
    E = (max-min)/mean*100
    return E


def map_uniformity(image, filtering=True):
    if filtering:
        image = box_filter(image, 3)
        image = box_filter(image, 7)

    max = np.max(image)
    min = np.min(image)

    map = image  # - min
    map = 1.0/(map / np.min(map))

    return map


def fun_lin(x, *p):
    return p[0] + p[1]*x


def fun_init_helper_lin(x_data, y_data):
    x_min = np.min(x_data)
    x_max = np.max(x_data)
    y_min = np.min(y_data)
    y_max = np.max(y_data)

    a = (y_max-y_min)/(x_max-x_min)
    b = a*x_min-y_min

    return b, a


def fun_exp(x, *p):
    return p[0] + p[1]*np.exp(p[2]*x)


def fit_curve(x_data, y_data, fun=fun_lin, range=(0, 100)):
    x_min = np.min(x_data)
    x_max = np.max(x_data)

    index_w = (x_data <= x_max*range[1]/100)*(x_data >= x_max*range[0]/100)
    y_data_w = y_data[index_w]
    x_data_w = x_data[index_w]

    popt, pcov = optimize.curve_fit(
        fun, x_data_w, y_data_w, fun_init_helper_lin(x_data_w, y_data_w))

    return popt, pcov
