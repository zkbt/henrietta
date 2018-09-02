
def get_lightcurve(star='Kepler-186', quarter=1, kind='PDCSAP_FLUX'):
    '''
    This function is a wrapper to download a single quarter of Kepler
    lightcurve and extract the PDCSAP_FLUX from it.
    '''

    (maybe it looks something like this?)
    lcf = lightkurve.KeplerLightCurveFile.from_archive(star)
    lcf = lightkurve.KeplerLightCurveFile.from_archive(star, quarter=quarter)
    lcf.plot()
    lc = lcf.get_lightcurve(kind)
    lc.plot()

def get_all_lightcurves(star='Kepler-42'):
    '''
    This function downloads all quarters of Kepler light curves, and
    stitches them together.
    '''
