import numpy as np, matplotlib.pyplot as plt
from scipy.stats import poisson, norm
from lightkurve import LightCurve



def create_photon_lightcurve(N=1):

    cadence = 1.0/60/60/24
    duration = 1.0
    t = np.arange(0, duration, step=cadence)
    photons = poisson.rvs(N, size=t.shape)
    lc = LightCurve(time=t,
                    flux=photons,
                    flux_err=np.sqrt(photons),
                    meta=dict(name='Poisson light curve with {} photons/s'.format(N)))
    return lc

# write this as its own lightcurve class?
# a light curve that includes a projected histogram?
# write a Gaussian one
