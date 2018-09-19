from ..modeling import *
from ..statistics import *

def test_batman():
    '''
    This function tests the batman transit light curve model.
    '''
    example_transit_model()

def test_residuals(N=1e6, duration=1000, **kw):
    lc = create_photon_lightcurve(N=N, duration=duration).normalize()
    plot_with_transit_model(lc, **kw)
