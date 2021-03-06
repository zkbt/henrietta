from astropy.modeling import models, fitting, optimizers, statistic, custom_model
import numpy as np
import emcee
import batman
import corner as triangle
import matplotlib.pyplot as plt

"""

This script takes in an astropy transit model and a lightkurve object,
determines which parameters are variable, and runs an MCMC
to fit those parameters and create a maximum likelihood model.

"""

def lnprob(params, astropy_model, lc):

    """
    Determine which parameters are variable, and set their value to the
    current parameter value in the chain.
    -----------
    """
    n = len(astropy_model.param_names)

    i = 0
    for k in astropy_model.param_names:
        if astropy_model.fixed[k] == False:
            for m in range(n):
                if astropy_model.param_names[m] == str(k):
                    astropy_model.parameters[m] = params[i]
                    i += 1

    if (astropy_model.a <= astropy_model.b):
        astropy_model.a = astropy_model.b + 0.01

    """
    Create the new model and calculate the log probability for a Gaussian
    likelihood.
    ------------
    """
    model = astropy_model(lc.time)

    if (0.0 <= astropy_model.radius <= 1.0) and (lc.time[0] <= astropy_model.t0 <= lc.time[-1] ) and (1.0 <= astropy_model.a <= 200.0 ):
        chisq = np.nansum((lc.flux - model)**2/(lc.flux_err)**2)
        lnp = np.nansum(1/np.sqrt(2*np.pi*(lc.flux_err))) - 0.5*chisq

        return lnp

    return -np.inf

def mcmc_fit(astropy_model, lc, nsteps = 10000, saveplots=False):

    '''
    This function will employ a Markov-Chain Monte Carlo to fit any number
    of free parameters to an exoplanet transit light curve.


    Parameters
    ----------

    lc: LightCurve object
        This is a `lightkurve`-style LightCurve object, which contains
        the attributes `lc.time` (times in JD) and `lc.flux` (the brightness
        of the star), as well as lots of methods for analysis and plotting.

    astropy_model: An 'astropy model' object
        This model obect contains all the model parameters, their names,
        and their bounds if they are free parameters. It interfaces
        with a custom model to generate the function of interest,
        which is a BATMAN light curve model in this case.


    Returns
    -------

    max_likelihood: A dictionary
        This dictionary contains the names of the variable parameters,
        as well as a 3-element list of the maximum likelihood value,
        and +/- 1 sigma uncertainties.

    sampler: EnsembleSampler Object
        This object has several capabilities. In this MCMC, it is primarily
        used to run the emcee function and give us access to sample parameter
        values generated by the Monte Carlo.

    '''

    """
    First, check that the lc object is normalized and folded. If not,
    fold and normalize it.
    ----------
    """

    fold_check = input(["Is your light curve folded? (y/n)"])

    if fold_check == "n":
        lc = lc.fold(period = astropy_model.period.value)
        print("That's okay, I did it for you")

    norm_check = input(["Is your light curve normalized? (y/n)"])

    if norm_check == "n":
        lc = lc.normalize()
        print("Do I have to do everything?")

    """
    Determine the names of all variable parameters, so that we can use
    these names later.
    ----------
    """

    variable_names = []
    i = 0
    for k in astropy_model.param_names:
        if astropy_model.fixed[k] == False:
            variable_names.append(str(k))
            i += 1

    """
    Create an organized parameter dictionary so that we can easily
    populate some initial parameter values, and then define an array
    of these initial values, to be input into emcee.
    ----------
    """

    organized = dict(period = astropy_model.period, t0 = astropy_model.t0,
                 radius = astropy_model.radius, a = astropy_model.a,
                 b = astropy_model.b, baseline = astropy_model.baseline,
                 ld1 = astropy_model.ld1, ld2 = astropy_model.ld2)

    ndim, nwalkers, nsteps = i, 100, nsteps
    burnin = int(0.2*nsteps)

    param_initial = []
    for k in astropy_model.param_names:
        if organized[k].fixed == False:
            bounds = organized[k].bounds
            organized[k].initialwalkers = np.random.uniform(bounds[0],bounds[1],nwalkers)
            param_initial.append(organized[k].initialwalkers)

    p0 = np.transpose(param_initial)

    """
    Create a sampler object and run the MCMC.
    ----------
    """

    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[astropy_model, lc])
    result = sampler.run_mcmc(p0, nsteps)

    samples = sampler.chain[:, burnin:, :].reshape((-1, ndim))

    """
    Set up the max_likelihood dictionary and populate it with the sample
    results. Then, plot each free parameter value as a function of the
    step in the chain each walker is at. This will show us whether or not
    parameters are converging, and at which values.
    ----------
    """

    max_likelihood = {}

    fig,ax = plt.subplots(i, 1, sharex=True, figsize=(8, 9))
    for j in range(i):
        param_samples = sampler.flatchain[int(nsteps*nwalkers/i):,j]
        max_likelihood[variable_names[j]] = np.percentile(param_samples, [16., 50., 84.])

        ax[j].plot(sampler.chain[:, :, j].T, color="k", alpha=0.4)
        ax[j].set_ylabel(variable_names[j])
        if j == i-1:
            ax[j].set_xlabel('Steps')
    if saveplots == True:
        plt.savefig('walker_plot.pdf', clobber=True)

    """
    Set up a corner plot, which will show us contour plots for each pair
    of parameters.
    ----------
    """

    ndim = i
    labels = variable_names

    fig, axes = plt.subplots(ndim, ndim, figsize=(13,13))
    triangle.corner(samples, bins=20, labels=labels,
                      max_n_ticks=3,plot_contours=True,quantiles=[0.16,0.5,0.84],fig=fig,
                      show_titles=True,verbose=True,range=None)

    if saveplots == True:
        plt.savefig('corner_plot.pdf', clobber=True)

    """
    Finally, set the model parameters to the maximum likelihood values and
    produce a plot of the data with that best fit model.
    ----------
    """

    n = len(astropy_model.param_names)
    i = 0
    for k in astropy_model.param_names:
        if astropy_model.fixed[k] == False:
            for m in range(n):
                if astropy_model.param_names[m] == str(k):
                    astropy_model.parameters[m] = max_likelihood[k][1]
                    i += 1

    plt.figure()
    lc.errorbar(alpha= 0.5,zorder=0,label='Data')
    plt.plot(lc.time,astropy_model(lc.time),zorder=100,
                label='Maximum Likelihood Model',
                color='b')
    plt.title('Light Curve with Maximum Likelihood Model')
    plt.legend()

    if saveplots == True:
        plt.savefig('Best-fit-model.pdf',clobber=True)

    return max_likelihood,sampler
