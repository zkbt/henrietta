from astropy.modeling import models, fitting, optimizers, statistic, custom_model
import numpy as np
import emcee
import batman

"""
Here I will write a function that takes in an astropy transit model and
a lightkurve object, determines which parameters have been determined to be fixed,
which are variable, and runs an MCMC with those parameters.

The astropy model already knows which parameters are fixed vs. variable,
I just need to figure out how to extract those parameters and set up an mcmc
which will adapt to however many free parameters are presentself.
"""

def lnprob(params):

    n = len(astropy_model.param_names)

    i = 0
    for k in astropy_model.fixed:
        if astropy_model.fixed[k] == False:
            for m in range(n):
                if astropy_model.param_names[m] == str(k):
                    astropy_model.parameters[m] = params[i]
                    i += 1

    model = astropy_model(lc.time)

    # This is a Gaussian likelihood, for independent data points

    if (0.0 <= astropy_model.radius <= 1.0) and (times[0] <= astropy_model.t0 <= times[-1] ) and (1.0 <= astropy_model.a <= 200.0 ):
        chisq = np.nansum((lc.flux - model)**2/(lc.flux_err)**2)
        lnp = np.nansum(1/np.sqrt(2*np.pi*(lc.flux_err))) - 0.5*chisq

        return lnp

    return -np.inf

def mcmc_fit(astropy_model, lc):

    #lc = lc.fold(period=astropy_model.period.value)
    #lc = lc.normalize()

    organized = dict(period = astropy_model.period, t0 = astropy_model.t0,
                 radius = astropy_model.radius, a = astropy_model.a,
                 b = astropy_model.b, baseline = astropy_model.baseline,
                 ld1 = astropy_model.ld1, ld2 = astropy_model.ld2)

    variable_names = []
    i = 0
    for k in astropy_model.fixed:
        if astropy_model.fixed[k] == False:
            variable_names.append(str(k))
            i += 1

    # intialize some walkers
    ndim, nwalkers, nsteps = i, 100, 5000
    burnin = int(0.2*nsteps)

    param_initial = []
    for k in organized:
        if organized[k].fixed == False:
            bounds = organized[k].bounds
            organized[k].initialwalkers = np.random.uniform(bounds[0],bounds[1],nwalkers)
            param_initial.append(organized[k].initialwalkers)

    p0 = np.transpose(param_initial)

    # create a sampler and run it
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob)
    result = sampler.run_mcmc(p0, nsteps)

    max_likelihood = {}

    for j in range(i):
        param_samples = sampler.flatchain[int(nsteps*nwalkers/i):,j]
        max_likelihood[variable_names[j]] = np.percentile(param_samples, [16., 50., 84.])

    return max_likelihood,sampler
