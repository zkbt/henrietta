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

    model = How am I actually calculating the batman modeL?

    # This is a Gaussian likelihood, for independent data points

    if (0.0 <= rp <= 1.0) and (times[0] <= t_0 <= times[-1] ):
        chisq = np.sum((lc.flux - model)**2/(lc.flux_err)**2)
        lnp = np.sum(1/np.sqrt(2*np.pi*(lc.flux_err))) - 0.5*chisq

        return lnp

    return -np.inf

def mcmc_fit(astropy_model, lc):

    period = astropy_model.period.value
    t0 = astropy_model.t0.value
    radius = astropy_model.radius.value
    a = astropy_model.a.value
    b = astropy_model.b.value
    baseline = astropy_model.baseline.value
    ld1 = astropy_model.ld1.value
    ld2 = astropy_model.ld2.value

    i = 0
    for k in astropy_model.fixed:
        if astropy_model.fixed[k] == False:
            i += 1

    # intialize some walkers
    ndim, nwalkers, nsteps = i, 100, 10000
    burnin = int(0.2*nsteps)

    # these are initial parameters
    param_initial = np.random.uniform(param[0], param[1], nwalkers)
    'How to set up the initial parameters?'

    p0 = np.transpose([param_initial])

    # create a sampler and run it
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)
    result = sampler.run_mcmc(p0, nsteps)

    max_likelihood = {}

    for j in range(i):
        param_samples[j] = sampler.flatchain[int(nsteps*nwalkers/i):,j]
        max_likelihood[variable_names[j]] = np.percentile(param_samples[j], [16., 50., 84.])

    return max_likelihood,sampler
