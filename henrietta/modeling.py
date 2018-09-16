import numpy as np
import matplotlib.pyplot as plt
import batman
import lightkurve
import lightkurve.LightCurve

def BATMAN(Baseline = 1.0, #units are whatever your flux units come in
           radius = 0.01, #Rp/R*
           per = 0.5, #days
           a = 10.0, #semi-major axis in a/R*
           t0 = 0, #time of inferior conjunction
           LD = [0.1956, 0.3700] #using GJ1132b params
           t = None):

    P = per * 24.0 #convert to hours

    params = batman.TransitParams()
    params.t0 = t0                      #time of inferior conjunction ()
    params.per = P              #period in hours
    params.rp = radius         #planet radius (in units of stellar radii)
    params.a = a                      #semi-major axis (in units of stellar radii)
    params.inc = 90.                     #orbital inclination (in degrees)
    params.ecc = 0.                      #eccentricity
    params.w = 90.                       #longitude of periastron (in degrees)
    params.u = LD         #limb darkening coefficients [u1, u2]
    params.limb_dark = "quadratic"       #limb darkening model

    m = batman.TransitModel(params, t)    #initializes model

    flux = m.light_curve(params)*Baseline       #calculates light curve

    return flux

def transit_model(lc, period, Rp, a = 10.0, baseline = 1, t0 = 0,
                ld = [0.1956, 0.3700], planet_name='Some planet, hopefully'):
    '''
    This function will take in a lightcurve for a planet
    with a given period (in hours), Rp/R*, Baseline, and
    mid-transit time (same units as lc.time) and will plot a
    batman light curve model. Limb-darkening coefficients can also be
    specified in the form [u1,u2]
    '''

    date = lc.time
    flux = lc.flux
    flux_err = lc.flux_err

    highres_time = np.linspace(date[0],date[-1],300)

    model_flux = BATMAN(Baseline = baseline,
                radius = Rp, #Rp/R*
                per = period, #days
                a = a, #semi-major axis in a/R*
                t0 = t0, #time of inferior conjunction
                LD = ld #using GJ1132b params
                t = date)

    model_plot = BATMAN(Baseline = baseline,
                radius = Rp, #Rp/R*
                per = period, #days
                a = a, #semi-major axis in a/R*
                t0 = t0, #time of inferior conjunction
                LD = ld #using GJ1132b params
                t = highres_time)

    plt.figure()
    plt.errorbar(date,flux,yerr=flux_err,fmt='o',alpha=0.5)
    plt.plot(highres_time,model_plot,zorder=100,color='k',label='I AM BATMAN')
    plt.title(planet_name)
    plt.xlabel('Time')
    plt.ylabel('Relative Flux')
    plt.legend()
    plt.show()
