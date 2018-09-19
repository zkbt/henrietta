import numpy as np

def stellar_density(P, jeff):

   '''
   P = planet orbital period in days
   jeff = ratio of planet semi-major axis to stellar radius
   '''

   G = 6.67e-11 #[m^3/(kg*s^2)]

   print('The density of your star is {} g/cm^3. Sweet.'.format(np.round(((3*np.pi/G) * (1/(P*60*60*24)**2) * (jeff)**3)/1000,2)))