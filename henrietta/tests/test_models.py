from ..modeling import *
from ..statistics import *
from ..goodnesses import *

def test_batman():
    '''
    This function tests the batman transit light curve model.
    '''
    example_transit_model()

def test_residuals(N=1e6, duration=10, cadence=1.0/60.0/24.0, period=3.14, t0=0.5, **kw):
    for e in [True, False]:
        lc = simulate_transit_data(N=N, duration=duration, cadence=cadence, period=period, t0=t0, **kw)
        plot_with_transit_model(lc, period=period, t0=t0, show_errors=e, **kw)

        folded = lc.fold(period=period, phase=t0/period)
        plot_with_transit_model(folded, period=period, t0=t0, show_errors=e, **kw)

    return lc, folded


def test_goodness(N=1e6, duration=10, cadence=1.0/60.0/24.0, period=3.14, t0=0.5, **kw):

    lc = simulate_transit_data(N=N, duration=duration, cadence=cadence, period=period, t0=t0,  **kw)
    folded = lc.fold(period=period, phase=t0/period)
    return plot_with_transit_model(folded, period=period, t0=t0, goodness=chisq, **kw)
