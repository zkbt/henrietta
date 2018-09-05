from henrietta import *

def test_download_kepler_lc():
    '''
    This function tests the wrapper for downloading
    a single quarter of Kepler data.
    '''

    lc = download_kepler_lc('Kepler-17')
    lc.plot(marker='.', linewidth=0)
    folded = lc.fold(1.48571092)
    folded.plot(marker='.', linewidth=0)
