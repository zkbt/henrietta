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

    Returns
    -------

    lc: LightCurve object
        This is a `lightkurve`-style LightCurve object, which contains
        the attributes `lc.time` (times in JD) and `lc.flux` (the brightness
        of the star), as well as lots of methods for analysis and plotting.

    '''

    # download a KeplerLightCurveFile from the MAST archive
    lcf = KeplerLightCurveFile.from_archive(star,
                                            quarter=quarter,
                                            cadence=cadence,
                                            quality_bitmask=quality_bitmask)

    # if a list, stitch things together (crudely! will be terrible for SAP!)
    if type(lcf) == list:

        # make a normalized light curve from the first light curve file
        lc = lcf[0].get_lightcurve(kind).normalize()

        # append the normalized light curves from all other light curve files
        for f in lcf[1:]:
            thisquarter = f.get_lightcurve(kind)
            lc = lc.append(thisquarter.normalize())

    # if a single quarter, simply return that light curve
    else:
        lc = lcf.get_lightcurve(kind)

    # return the light curve
    return lc



def locate_transits(lc, period, epoch):

    '''

    This function takes in a lightcurve object along with the planet's
    period and epoch in order to identify on the plot each expected location
    of a transit

    lc should be a lightkurve object which has (B)JD times and fluxes.
    period should be in days
    epoch must be in JD or BJD


    It will return the JD times of 200 post-epoch transits

    '''

    n = np.linspace(0,199,200)
    transit_loc = n*period + epoch

    time = lc.time
    flux = lc.flux

    avg_flux = np.median(flux)

    fig,ax = plt.subplots()
    plt.title('Transit locations')
    plt.xlabel('Time (JD)')
    plt.ylabel('Flux')
    plt.xlim(time[0],time[-1])
    plt.scatter(time,flux)
    for i in range(len(n)):
        if (transit_loc[i] >= np.amin(time)) and (transit_loc[i] <= np.amax(time)):
            plt.axvspan(xmin=transit_loc[i]-0.05*(time[-1]-time[0]),
            xmax=transit_loc[i]+0.05*(time[-1]-time[0]),color='green',alpha=0.4)
            #circle = plt.Circle((0,0),radius=1,fill=False,color='purple',alpha=0.4,linewidth=5)
    #ax.add_artist(circle)
    plt.show()


    return transit_loc


def extract_transits(lc, period, epoch, duration, baseline):

    time = lc.time
    flux = lc.flux


    return transits, notransits
