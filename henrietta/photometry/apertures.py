'''
Define an Aperture object, which
    -has a location
    -does photometry
    -can be plotted and picked
    -can be unplotted
'''

from ..imports import *
import photutils
from astropy.stats import sigma_clipped_stats
from astropy.table import Table


class InteractiveAperture(photutils.CircularAperture):

    def __init__(self, name='', pos=(0,0), loupe=None,  aperture_radius=5, background_radii=[15, 25], subtract_background=False):

        # initialize the CircularAperture as normal
        photutils.CircularAperture.__init__(self, pos, aperture_radius)

        # create a background aperture
        r_in, r_out = background_radii
        self.background_aperture = photutils.CircularAnnulus(pos, r_in, r_out)
        self.subtract_background = subtract_background

        # keep track of this aperture's name
        self.name = name

        # keep track of the loupe this aperture is a part of
        self.loupe = loupe

        # keep track of the flux in this aperture with an undefined flux
        self.flux = np.nan

    def plot(self, ax):
        '''
        Plot this aperture onto the given axes.
        '''

        # create an empty dictionary to store any plots
        self.plotted = {}

        # (this can handle only single-position apertures)
        pos = self.positions[0]

        # (pull out the apeture radius)
        aperture_radius = self.r

        # create the circle
        self.plotted['circle'] = plt.Circle(pos, aperture_radius, color='black',fill=False,zorder=100,linewidth=2, picker=True)
        ax.add_artist(self.plotted['circle'])
        self.plotted['marker'] = plt.scatter(pos[0], pos[1], marker='+', alpha=0.3, color='black')
        self.plotted['label'] = plt.text(pos[0]+aperture_radius+1, pos[1], self.name, va='center', zorder=11, color='black')


        r_in, r_out = self.background_aperture.r_in, self.background_aperture.r_out
        bgkw = dict(color='black', alpha=0.3, fill=False, zorder=100)

        self.plotted['background_inner_circle'] = plt.Circle(pos, r_in, **bgkw)
        self.plotted['background_outer_circle'] = plt.Circle(pos, r_out, **bgkw)

        for k in ['background_inner_circle', 'background_outer_circle']:
            ax.add_artist(self.plotted[k])
            self.plotted[k].set_visible(self.subtract_background)

    def erase(self):
        '''
        Remove any traces of this aperture from the plot.
        '''
        for k in self.plotted.keys():
            self.plotted[k].remove()

    def update(self):
        '''
        After a plot has already been created, update its hidden properties,
        as well as its appearance on the interactive plot.
        '''

        # update the radius
        self.r = self.loupe.aperture_radius
        self.background_aperture.r_in, self.background_aperture.r_out = self.loupe.background_radii
        self.subtract_background = self.loupe.subtract_background


        # update the plot
        pos = self.positions[0]
        self.plotted['circle'].set_radius(self.r)
        self.plotted['label'].set_position((pos[0]+self.r+1, pos[1]))
        self.plotted['marker'].set_offsets(pos)
        self.plotted['background_inner_circle'].set_radius(self.background_aperture.r_in)
        self.plotted['background_outer_circle'].set_radius(self.background_aperture.r_out)

        for k in ['background_inner_circle', 'background_outer_circle']:
            self.plotted[k].set_visible(self.subtract_background)

        self.table = Table(data=[[self.name], [pos[0]], [pos[1]], [0.0]], names=['#','x', 'y', 'flux'])
        # do the photometry in the aperture
        aperture, _ = self.do_photometry(self.loupe.image)

        if self.subtract_background:

            # calculate the background flux
            background_mask = self.background_aperture.to_mask(method='center')[0]
            background_masked_image = background_mask.multiply(self.loupe.image)
            values = background_masked_image[background_masked_image != 0]
            _, background_median, _ = sigma_clipped_stats(values)
            aperture_background = background_median*self.area()
            aperture -= aperture_background
            self.table['sky'] = aperture_background
            self.table['sky'].format = '.2e'

        self.table['flux'] = aperture

        self.table['x'].format = '.0f'
        self.table['y'].format = '.0f'
        self.table['flux'].format = '.2e'

    #def __str__(self):
    #    '''
    #    How should this aperature appear as a string (for example, if it is
    #    included in a `'{}'.format()` statement)?
    #    '''
    #    #return '{:>8} at ({:4.1f}, {:4.1f}) sums to {:10.1f} (area of {:.1f} pixels).'.format(self.name, self.positions[0][0], self.positions[0][1],  self.flux, self.area())
    #    return repr(self.table)

class ApertureWithBackground(InteractiveAperture):
    pass
    #def __init__(self, name='', pos=(0,0), aperture_radius=3 ):
    #    pass
