import numpy as np
import matplotlib.pyplot as plt

try:
    import batman
except:
    print("""
    `batman-package` is not installed on this computer.

    You can use most of the henrietta tools with no problem,
    but you will not be able to generate transit models :-(
    """)
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

def transit_model(lc, period, Rp, a = 10.0, baseline = 1, t0 = 0,
                ld = [0.1956, 0.3700], planet_name='Some planet, hopefully',
                plot_residuals = False):
    '''
    This function will take in a lightcurve for a planet
    with a given period (in hours), Rp/R*, baseline, and
    mid-transit time (same units as lc.time) and will plot a
    batman light curve model. Limb-darkening coefficients can also be
    specified in the form [u1,u2]
    '''

    date = lc.time
    flux = lc.flux
    flux_err = lc.flux_err

    highres_time = np.linspace(date[0],date[-1],300)


    model_flux = BATMAN(baseline = baseline,
                radius = Rp, #Rp/R*
                period = period, #days
                a = a, #semi-major axis in a/R*
                t0 = t0, #time of inferior conjunction
                ld = ld, #using GJ1132b params
                t = date)

    model_plot = BATMAN(baseline = baseline,
                radius = Rp, #Rp/R*
                period = period, #days
                a = a, #semi-major axis in a/R*
                t0 = t0, #time of inferior conjunction
                ld = ld, #using GJ1132b params
                t = highres_time)

    f, (a0, a1) = plt.subplots(1,2, gridspec_kw = {'height_ratios':[4, 1]})
    a0.errorbar(date,flux,yerr=flux_err,fmt='o',alpha=0.5)
    a0.plot(highres_time,model_plot,zorder=100,color='k',label='I AM BATMAN')
    plt.title(planet_name)
    plt.xlabel('Time')
    plt.ylabel('Relative Flux')
    plt.legend(frameon=False)
    if plot_residuals:
        a1.scatter(date,(model_flux-flux))
        a1.axhline(0)
    plt.show()

    return highres_time,model_plot
