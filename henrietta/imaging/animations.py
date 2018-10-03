from ..imports import *
import illumination as il
import astropy.units as u

def animate_tpf(tpf, howmanydays=None):
    '''
    Create a .mp4 animation of the data in a TPF.

    Parameters
    ----------
    tpf : KeplerTargetPixelFile
        A time series of pixels.

    howmanydays : float
        The maximum number of days to animate.
    '''

    # create a sequence of images
    seq = il.make_image_sequence(tpf.flux, time=tpf.time)

    # create a frame of the raw data
    frame = il.imshowFrame(data=seq, title='{} | {}'.format(tpf.mission, tpf.targetid))

    # create a frame with the subtracted data
    diff = il.imshowFrame(data=seq, title='difference', processingsteps=['subtractmedian'])

    #
    illustration = il.GenericIllustration(imshows=[frame, diff], sharecolorbar=False)
    filename = '{}-{}-animated.mp4'.format(tpf.mission, tpf.targetid)
    if howmanydays is None:
        maxtimespan = None
    else:
        maxtimespan = howmanydays*u.day
    illustration.animate(filename=filename, cadence=seq.cadence(), maxtimespan=maxtimespan)
