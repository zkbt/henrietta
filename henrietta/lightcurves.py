from lightkurve import KeplerLightCurveFile
import matplotlib.pyplot as plt
import numpy as np

def download_kepler_lc(star='Kepler-186',
                       quarter='all',
                       cadence='long',
                       quality_bitmask='hard',
                       kind='PDCSAP_FLUX'):
    '''
    This function is a wrapper to download a single quarter of Kepler
    lightcurve data, and extract a LightCurve object from it.

    When downloading a Kepler LightCurveFile from online, we get lots
    of information, including multiple different kinds of light curves
    for the same star. The goal of this little wrapper is to make it
    easy to get just one single light curve to play with.

    This has been tested only on data from the main Kepler mission.
    For K2 data, you may need to download a TPF.

    Parameters
    ----------

    star: str, int
        The name of the star whose light curve you want to download.
        This can be a name ("Kepler-42", "KOI-961") or a KIC number
        (8561063)

    quarter: str, int
        Which Kepler quarter to download?
            'all' = download the entire mission of data
            1, 2, 3 ... = download a specific quarter

    cadence: str
        'long' for Kepler long cadence
        'short' for Kepler short cadence

    quality_bitmask: str, int
        'none' = ignore no data
        'default' = ignore data with serious quality issues
        'hard' = be a little more cautious in what we call good data
        'hardest' = be too cautious about what we call good data

    kind: str
        "SAP_FLUX" = simple aperture photometry
        "PDCSAP_FLUX" = SAP, with pre-search data conditioning applied,
                        to get rid of some instrumental systematics
                        from the light curves (but watch out! some
                        astrophysical signals might be messed up too!)

    '''

    # download a KeplerLightCurveFile from the MAST archive
    lcf = KeplerLightCurveFile.from_archive(star,
                                            quarter=quarter,
                                            cadence=cadence,
                                            quality_bitmask=quality_bitmask)

    # if a list, stitch things together (crudely! will be terrible for SAP!)
    if type(lcf) == list:
        lc = lcf[0].get_lightcurve(kind).normalize()
        for f in lcf[1:]:
            thisquarter = f.get_lightcurve(kind)
            lc = lc.append(thisquarter.normalize())
    # if a single quarter, simply return that light curve
    else:
        lc = lcf.get_lightcurve(kind)
    return lc
