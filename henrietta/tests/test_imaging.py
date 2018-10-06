from ..imports import *
from ..imaging import animations, io, simulations
from ..utilities import mkdir

directory = 'examples'
mkdir(directory)

def test_io():
    '''
    This tests the tools for reading and writing images.
    '''

    # create a test image
    xsize, ysize = 200, 100
    x = np.arange(xsize)
    image = np.random.normal(0, 1, (ysize, xsize))

    for suffix in ['png', 'jpg', 'tif', 'gif']:
        filename = os.path.join(directory, 'image.{}'.format(suffix))
        io.write_image(image, filename=filename)
        gray = io.read_gray(filename)
        r, g, b = io.read_rgb(filename)
        
