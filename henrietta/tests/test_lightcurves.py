from ..lightcurves import *

def test_download_kepler_lc():
    '''
    This function tests the wrapper for downloading
    a single quarter of Kepler data.
    '''

    lc = download_kepler_lc('Kepler-17')
    lc.plot(marker='.', linewidth=0)
    folded = lc.fold(1.48571092)
    folded.plot(marker='.', linewidth=0)

def test_locate():
    '''
    This function should draw a single circle
    around every transit in the Kepler-17 light curve.
    '''
    lc = download_kepler_lc('Kepler-17')
    lc.plot(marker='.', linewidth=0)
    locate_transits(lc, period=1.4857108, epoch=2455185.678035)
