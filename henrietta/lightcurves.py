
def get_lightcurve(star='Kepler-42', quarter=1, kind='PDCSAP_FLUX'):
    '''
    This function is a wrapper to download a single quarter of Kepler
    lightcurve and extract the PDCSAP_FLUX from it.
    '''

    (maybe it looks something like this?)
    lcf = lightkurve.KeplerLightCurveFile.from_archive('Kepler-186')
    lcf = lightkurve.KeplerLightCurveFile.from_archive('Kepler-186', quarter=1)
    lcf.plot()
    lc = lcf.get_lightcurve('PDCSAP_FLUX')
    lc.plot()
    print("hello")

def get_all_lightcurves(star='Kepler-42'):
    '''
    This function downloads all quarters of Kepler light curves, and
    stitches them together.
    '''
