from ..modeling import *
from ..statistics import *

def test_batman():
    '''
    This function tests the batman transit light curve model.
    '''
    example_transit_model()

def test_residuals(N=1e6, duration=1000, **kw):
    lc = simulate_transit_data(N=N, duration=duration, **kw)
    plot_with_transit_model(lc, **kw)
