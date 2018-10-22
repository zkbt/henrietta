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

def Limb_Dark(Teff=star_teff,Terr=100,log_g=planet_g,g_err=0.1,met=planet_met,met_err=0.01):

    filters = [kepler]

    sc = LDPSetCreator(filters=filters,
                   teff=[Teff,Terr],
                   logg=[log_g, g_err],
                   z=[met, met_err])

    ps = sc.create_profiles(nsamples=500)
    qc,qe = ps.coeffs_qd(do_mc=True)

    LD_coeff = qc

    return LD_coeff

LD_coeff = Limb_Dark(Teff = star_teff, log_g = planet_g, met = planet_met)
LD = [LD_coeff[0][0],LD_coeff[0][1]]

def BATMAN(Baseline = 1.0, # units are whatever your flux units come in
           Rp = planet_radius,
           P = planet_period,
           a = planet_a,
           b = planet_b,
           t0 = expected_t0,
           t = None):

    params = batman.TransitParams()
    params.t0 = t0                       # time of inferior conjunction ()
    params.per = P                       # period in hours
    params.rp = Rp                       # planet radius (in units of stellar radii)
    params.a = a                         # semi-major axis (in units of stellar radii)
    params.inc = np.arccos(b/a)*180/np.pi   # orbital inclination (in degrees)
    params.ecc = 0.                      # eccentricity
    params.w = 90.                       # longitude of periastron (in degrees)
    params.u = LD                        # limb darkening coefficients [u1, u2]
    params.limb_dark = "quadratic"       # limb darkening model

    m = batman.TransitModel(params, t)   # initializes model

    flux = m.light_curve(params)*Baseline   # calculates light curve

    return flux

def lnprob(parameters, plot = False, extra_mods = False,
           Title = planet_name, Rp_best = 0, Rp_diff = 0,
           t0_best = 0, t0_diff = 0):

    # Pull out some model parameters
    rp, t_0 = parameters

    # First we want a model to perform the lnprob calculation with.
    model = BATMAN(Rp = rp, t0 = t_0, t = lc.time)

    residual = (model-lc.flux)/lc.flux_err

    # This is the model that will be plotted
    model_to_plot = BATMAN(Rp = rp, t0 = t_0, t = times)

    if plot:

        f, (a0, a1) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[4,1]},
                                   figsize=(10,7),sharex=True)

        a0.set_title(Title,fontsize=20)
        a0.errorbar(lc.time,lc.flux,yerr=lc.flux_err,fmt='o',alpha=0.5,color='royalblue',
                    markersize='5',label=observatory+' data')
        a0.plot(times,model_to_plot,label='MCMC Model',color='k',zorder=100)
        a0.plot(times,alert_model,label='Preliminary Parameters',color='purple',zorder=99)
        a0.set_ylabel('Flux',fontsize=18)

        a1.scatter(lc.time,residual,color='royalblue',alpha=0.5,label='Residuals')
        a1.axhline(0,color='k')
        a1.set_ylim(0-1.5*np.max(np.abs(residual)),0+1.5*np.max(np.abs(residual)))

        if extra_mods:
            y1 = BATMAN(Rp=rp, t0 = t_0+t0_diff, t = times)
            y2 = BATMAN(Rp=rp, t0 = t_0-t0_diff, t = times)
            a0.fill_between(times,y1,y2,label='1-$\sigma$ Models',
                            alpha=0.5,color='red',zorder=100)
            y1 = BATMAN(Rp = rp+Rp_diff, t0 = t_0, t = times)
            y2 = BATMAN(Rp = rp-Rp_diff, t0 = t_0, t = times)
            a0.fill_between(times,y1,y2,alpha=0.5,color='red',zorder=100)

        a0.legend()
        a1.legend()
        plt.xlabel('BJD - '+str(offset),fontsize=16)
        plt.savefig(planet_name+'-model.pdf')

    # This is a Gaussian likelihood, for independent data points

    if (0.0 <= rp <= 1.0) and (times[0] <= t_0 <= times[-1] ):
        chisq = np.sum((lc.flux - model)**2/(lc.flux_err)**2)
        lnp = np.sum(1/np.sqrt(2*np.pi*(lc.flux_err))) - 0.5*chisq

        return lnp

    return -np.inf

def mcmc_fit(astropy_model, lc):

    parameters = astropy_model.params()

    pull out parameter values and whether or not they are fixed

    for k in model.fixed.keys():
        print(model.fixed[k])


    # intialize some walkers
    ndim, nwalkers, nsteps = 2, 100, 10000
    burnin = int(0.2*nsteps)

    # these are initial parameters
    Rp_initial = np.random.uniform(rp_range[0], rp_range[1], nwalkers)
    t0_initial = np.random.uniform(t0_range[0], t0_range[1], nwalkers)

    p0 = np.transpose([Rp_initial, t0_initial])

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
