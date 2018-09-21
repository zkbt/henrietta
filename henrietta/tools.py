import numpy as np

def stellar_density(P, jeff):

   '''
   P = planet orbital period in days
   jeff = ratio of planet semi-major axis to stellar radius
   '''

   G = 6.67e-11 #[m^3/(kg*s^2)]

   print('The density of your star is {} g/cm^3. Sweet.'.format(np.round(((3*np.pi/G) * (1/(P*60*60*24)**2) * (jeff)**3)/1000,2)))


kepler_offset = 2454833.0
tess_offset = 2457000.0

def bjd2bkjd(t):
    '''
    Convert a
    BJD (Barycentric Julian Date)
    into a
    BKJD (Barycentric Kepler Julian Date)
    via the relationship
    BKJD = BJD - 2454833.0
    '''
    return t - kepler_offset


def bkjd2bjd(t):
    '''
    Convert a
    BKJD (Barycentric Kepler Julian Date)
    into a
    BJD (Barycentric Julian Date)
    via the relationship
    BKJD = BJD - 2454833.0
    '''
    return t + kepler_offset

def bjd2btjd(t):
    '''
    Convert a
    BJD (Barycentric Julian Date)
    into a
    BTJD (Barycentric TESS Julian Date)
    via the relationship
    BTJD = BJD - 2457000.0
    '''
    return t - tess_offset


def btjd2bjd(t):
    '''
    Convert a
    BTJD (Barycentric TESS Julian Date)
    into a
    BJD (Barycentric Julian Date)
    via the relationship
    BTJD = BJD - 2457000.0
    '''
    return t + tess_offset
