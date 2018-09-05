
def download_kepler_lc(star='Kepler-186', quarter=1, kind='PDCSAP_FLUX'):
    '''
    This function is a wrapper to download a single quarter of Kepler
    lightcurve data, and extract a LightCurve object from it.
    
    When downloading a Kepler LightCurveFile from online, we get lots
    of information, including multiple different kinds of light curves
    for the same star. The goal of this little wrapper is to make it 
    easy to get just one single light curve to play with.
    
    Parameters
    ----------
    
    star : str, int
        The name of the star whose light curve you want to download.
        This can be a name ("Kepler-42", "KOI-961") or a KIC number
        (8561063)
        
    quarter : int
        Which Kepler quarter to download?
    
    kind : str
        "SAP_FLUX" = simple aperture photometry
        "PDCSAP_FLUX" = SAP, with pre-search data conditioning applied,
                        to get rid of some instrumental systematics 
                        from the light curves (but watch out! some
                        astrophysical signals might be messed up too!)
    
    '''

    lcf = lightkurve.KeplerLightCurveFile.from_archive(star, quarter=quarter)
    lc = lcf.get_lightcurve(kind)
    return lc

def get_all_lightcurves(star='Kepler-42'):
    '''
    This function downloads all quarters of Kepler light curves, and
    stitches them together.
    '''
