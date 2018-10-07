

from ..imports import *
from skimage import io
from astropy.io import fits

def read_fits(path, ext_image=1):
    '''
    Read an image from a FITS file.
    '''

    # open the fits file
    hdu_list = fits.open(path)

    # make sure we're asking for a reasonable image extension
    ext_image = np.minimum(ext_image, len(hdu_list)-1)

    # extract the image data from the FITs file
    image = hdu_list[ext_image].data

    print('read a {} grayscale image from {}'.format(image.shape, path))

    # return the image
    return image

def read_rgb(path):
    '''
    Read an image (.jpg, .png, .tif, .gif)
    into three numpy arrays, one each for
    the brightness in Red, Green, Blue.

    Parameters
    ----------
    path : str
        The filename of the image to read.

    Returns
    -------
    r, g, b : arrays
        The brightness of the image in each of the
        red, green, blue wavelength ranges.
    '''

    # read a (rows x cols x 3) image
    rgb = io.imread(path)

    # pull out the red, green, blue channels
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    # print an update
    print('read a {} RGB image from {}'.format(rgb.shape, path))

    # return the three separate images
    return r, g, b

def read_gray(path):
    '''
    Read an image (.jpg, .png, .tif, .gif)
    into one numpy array, where the individual
    RGB channels have been merged together
    into one single grayscale image.

    Parameters
    ----------
    path : str
        The filename of the image to read.

    Returns
    -------
    gray : array
        The brightness of the image, estimated
        from a weighted average across the red,
        green, and blue bandpasses.
    '''

    # load the image as gray-scale
    image = io.imread(path, as_gray=True)

    # print an update
    print('read a {} grayscale image from {}'.format(image.shape, path))

    # return the image
    return image

def write_image(image, filename='image.jpg'):
    '''
    Write a numpy a array to an image file.
    '''

    # print an update
    print('saved {} image to {}'.format(image.shape, filename))

    # save the image
    io.imsave(filename, image)

# read different image file types (png, tiff, giff)
# write a guesser to read an arbitrary image (based on filename)
# read a movies as a sequence of images (?)
# (add URL capability for the path)?
