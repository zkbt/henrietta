import numpy as np
import matplotlib.pyplot as plt
import batman
import lightkurve
from lightkurve import LightCurve

def BATMAN(t,
           period = 1.0, #days
           t0 = 0, #time of inferior conjunction
           radius = 0.1, #Rp/R*
           a = 10.0, #semi-major axis in a/R*
           b = 0.0, #impact parameter in stellar radii
           baseline = 1.0, #units are whatever your flux units come in
           ld = [0.1956, 0.3700], #using GJ1132b params
           ):
    '''
    This function returns a model transit light curve
    for a given array of times and set of parameters.
    It currently assumes a circular orbit.

    Parameters
    ----------
    t : array
        An array of times, in units of days.

    period : float
        The orbital period of the planet, in units of days.

    t0 : float
        One mid-transit time, in units of days.

    radius : float
        The radius of the planet, in units of stellar radii.
        (This is sometimes also called Rp/R*).

    a : float
        The orbital distance (semimajor axis) of the planet, in stellar radii.
        (This is sometimes also called a/R*).

    b : float
        The transit impact parameter of the planet, in stellar radii.
        (This is closely related to the inclination.)

    baseline : float
        The out-of-transit flux level, in whatever units you want.

    ld : list or array of floats
        The limb-darkening coefficients, for a quadratic limb-darkening.
    '''

    # create a batman transit parameter object
    params = batman.TransitParams()

    params.t0 = t0                      #time of inferior conjunction ()
    params.per = period             #period in days
    params.rp = radius         #planet radius (in units of stellar radii)
    params.a = a                      #semi-major axis (in units of stellar radii)
    params.inc = np.arccos(b/a)*180/np.pi                   #orbital inclination (in degrees)
    params.ecc = 0.                      #eccentricity
    params.w = 90.                       #longitude of periastron (in degrees)
    params.u = ld         #limb darkening coefficients [u1, u2]
    params.limb_dark = "quadratic"       #limb darkening model

    # initialize a batman model for the given times
    m = batman.TransitModel(params, t)

    # calculate a light curve (at the pre-set times)
    flux = m.light_curve(params)*baseline

    # return those light curve values
    return flux

def example_transit_model( period = 0.5, #days
                           t0 = 0, #time of inferior conjunction
                           radius = 0.01, #Rp/R*
                           a = 10.0, #semi-major axis in a/R*
                           b = 0.0, #impact parameter in stellar radii,
                           tmin=-0.5, tmax=0.5, cadence=1.0/60.0/24.0,
                           ylim=[0.985, 1.005],
                           ax=None):
    '''
    This function makes an example plot of a model transit light curve.

    Parameters
    ----------
    t : array
        An array of times, in units of days.

    period : float
        The orbital period of the planet, in units of days.

    t0 : float
        One mid-transit time, in units of days.

    radius : float
        The radius of the planet, in units of stellar radii.
        (This is sometimes also called Rp/R*).

    a : float
        The orbital distance (semimajor axis) of the planet, in stellar radii.
        (This is sometimes also called a/R*).

    b : float
        The transit impact parameter of the planet, in stellar radii.
        (This is closely related to the inclination.)

    tmin : float
        The minimum time to plot, in days.

    tmax : float
        The maximum time to plot, in days.

    cadence : float
        The cadence (time-step) to use, in days.

    ylim : list
        The ylimits for the plot.

    ax : matplotlib.axes object
        If an ax is fed in as a keyword argument, the plot
        will be added to that existing plot axes. To include
        multiple different models on the same plot, say:

        ax = example_transit_model()
        ax = example_transit_model(rp=0.042, ax=ax)
        ax = example_transit_model(rp=0.042, b=0.9, ax=ax)
        ...

    Returns
    -------

    plotted_ax : matplotlib.axes object
        The axes into which the model was was plotted.
    '''

    # create an array of times and flux values
    t = np.arange(tmin, tmax, cadence)
    f = BATMAN(t=t, period=period, t0=t0, radius=radius, a=a, b=b)

    # make a lightkurve LightCurve object
    model_lc = LightCurve(time=t, flux=f)

    # plot that, and set the ylimits
    plotted_ax = model_lc.plot(ax=ax, label='period={period},t0={t0},radius={radius},a={a},b={b}'.format(**locals()))
    plt.ylim(*ylim)

    # return the current axes, in case someone wants to plot into them again
    return plotted_ax

def plot_with_transit_model(lc,
                       period = 1.0, #days
                       t0 = 0, #time of inferior conjunction
                       radius = 0.1, #Rp/R*
                       a = 10.0, #semi-major axis in a/R*
                       b = 0.0, #impact parameter in stellar radii
                       baseline = 1.0, #units are whatever your flux units come in
                ld = [0.1956, 0.3700],
                planet_name='Some planet.'):
    '''
    This function will take in a lightcurve for a planet
    with a given set of transit parameters (period, t0, radius, a, b, baseline)
    and will plot a batman light curve model. Limb-darkening coefficients
    can also be specified in the form [u1,u2].

    Parameters
    ----------
    lc : LightCurve object
        Data contained in a lightkurve LightCurve object.

    period : float
        The orbital period of the planet, in units of days.

    t0 : float
        One mid-transit time, in units of days.

    radius : float
        The radius of the planet, in units of stellar radii.
        (This is sometimes also called Rp/R*).

    a : float
        The orbital distance (semimajor axis) of the planet, in stellar radii.
        (This is sometimes also called a/R*).

    b : float
        The transit impact parameter of the planet, in stellar radii.
        (This is closely related to the inclination.)

    baseline : float
        The out-of-transit flux level, in whatever units you want.

    ld : list or array of floats
        The limb-darkening coefficients, for a quadratic limb-darkening.
    '''

    # create a high-resolution grid of times to plot
    highres_time = np.arange(lc.time[0],lc.time[-1],2.0/60.0/24.0)

    # craete a model of the flux at the light curve times
    model_flux = BATMAN(baseline = baseline,
                radius = radius, #Rp/R*
                period = period, #days
                a = a, #semi-major axis in a/R*
                b = b,
                t0 = t0, #time of inferior conjunction
                ld = ld, #using GJ1132b params
                t = lc.time)

    # create a model of the flux at high resolution
    model_plot = BATMAN(baseline = baseline,
                radius = radius, #Rp/R*
                period = period, #days
                a = a, #semi-major axis in a/R*
                b = b,
                t0 = t0, #time of inferior conjunction
                ld = ld, #using GJ1132b params
                t = highres_time)

    # calculation the difference between the data and the model
    residual = (lc.flux - model_flux)

    f, (a0, a1) = plt.subplots(2,1, gridspec_kw = {'height_ratios':[4,1]},figsize=(10,7),sharex=True)
    a0.set_title(planet_name,fontsize=20)
    a0.set_ylabel('Flux',fontsize=18)
    a0.errorbar(lc.time,lc.flux,yerr=lc.flux_err,fmt='o',alpha=0.5,
            color='royalblue',markersize='5',label='Data')
    summary = 'BATMAN(period={period},t0={t0},radius={radius},a={a},b={b})'.format(**locals())
    a0.plot(highres_time,model_plot,zorder=100,color='k',label=summary)
    a0.legend()

    a1.scatter(lc.time,residual,color='royalblue',alpha=0.5,label='Residuals')
    a1.axhline(0,color='k')
    a1.set_ylim(0+1.5*np.max(np.abs(residual)),0-1.5*np.max(np.abs(residual)))
    a1.legend()

    plt.xlabel('Time (days)',fontsize=16)

    return highres_time,model_plot
