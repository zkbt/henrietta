from astropy.modeling import models, fitting, optimizers, statistic, custom_model
import pandas
import numpy as np
import matplotlib.pyplot as plt
import lightkurve
import emcee
import batman
from lightkurve.lightcurve import LightCurve
from ldtk import (LDPSetCreator,BoxcarFilter)
from ldtk.filters import kepler

"""
Here I will write a function that takes in an astropy transit model and
a lightkurve object, determines which parameters have been determined to be fixed,
which are variable, and runs an MCMC with those parameters.

The astropy model already knows which parameters are fixed vs. variable,
I just need to figure out how to extract those parameters and set up an mcmc
which will adapt to however many free parameters are presentself.
"""

def lnprob(parameters):

    #here, parameters is pulled from the astropy model object

    # Pull out some model parameters
    params = parameters #somehow I have to specify which fixed and floating params are used

    model = #call batman or the astropy model in order to calculate model flux

    # This is a Gaussian likelihood, for independent data points

    if (0.0 <= rp <= 1.0) and (times[0] <= t_0 <= times[-1] ):
        chisq = np.sum((lc.flux - model)**2/(lc.flux_err)**2)
        lnp = np.sum(1/np.sqrt(2*np.pi*(lc.flux_err))) - 0.5*chisq

        return lnp

    return -np.inf

def mcmc_fit(astropy_model, lc):

    parameters = astropy_model.params()

    pull out parameter values and whether or not they are fixed

    i = 0
    for k in model.fixed.keys():
        if model.fixed.keys()[k] == False:
            i += 1

    # intialize some walkers
    ndim, nwalkers, nsteps = i, 100, 10000
    burnin = int(0.2*nsteps)

    # these are initial parameters
    param_initial = np.random.uniform(param[0], param[1], nwalkers)

    p0 = np.transpose([param_initial])

    # create a sampler and run it
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)
    result = sampler.run_mcmc(p0, nsteps)

    Rp = sampler.flatchain[int(nsteps*nwalkers/2):,0]
    t0 = sampler.flatchain[int(nsteps*nwalkers/2):,1]

    sig1_Rp = np.percentile(Rp, [16., 50., 84.])
    print(sig1_Rp)
    sig1_t0 = np.percentile(t0, [16., 50., 84.])
    print(sig1_t0)

    return max_likelihood,sampler
