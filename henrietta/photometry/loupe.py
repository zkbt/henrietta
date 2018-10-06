from ..imports import *
import illumination as il
from IPython.display import display
import ipywidgets as widgets
import photutils

class Photometer:
    def __init__(self, image):

        self.image = image
        self.frame = il.imshowFrame(data=image)
        self.frame._pithy=True

        self.illustration = il.GenericIllustration(imshows=[self.frame])
        self.illustration._pithy=True



        # start with no apertures
        self.aperture_positions = []

        self.widge = widgets.interactive(self.photometry,
                                         ap_size=(0, 10),
                                         r_in=(0, 30),
                                         r_out=(0, 30),
                                         back_photo=False)
        display(self.widge)
        self.illustration.plot()
        # set it up so we can add or subtract an aperture by clicking on the image
        self.illustration.figure.canvas.mpl_connect('button_press_event', self.handle_click)


    def handle_click(self, event):
        '''
        If the user clicks on the imshow, do something with that click.

        Parameters
        ----------
        event : matplotlib.backend_bases.LocationEvent

        '''
        if event.button != 1:
            self.remove_aperture(event.xdata, event.ydata)
        else:
            self.add_aperture(event.xdata, event.ydata)
        self.widge.update()

    def add_aperture(self, x, y):
        '''
        Add an aperture at a particular (x, y) location.
        '''
        position = np.array([x,y])
        self.aperture_positions.append(position)

    def remove_aperture(self, x, y):
        '''
        Remove the closest aperture to the given (x,y) location.

        Parameters
        ----------
        x, y : float
            The location where we want to remove an aperture.
        '''
        xexisting, yexisting = np.array(self.aperture_positions).T
        distance = (xexisting - x)**2 + (yexisting - y)**2
        closest = np.argmin(distance)
        self.aperture_positions.pop(closest)


    def photometry(self, ap_size=10,r_in=20,r_out=30,back_photo=True):

        '''
        Create apertures around specified list of stars

        Parameters:
        -----------

        ap_size : int
            The radius of a circular aperture in pixel size
        r_in : int
            The inner radius of background aperture in pixel size
            (Ignore if back_photo=False)
        r_out : int
            The outer radius of background aperture in pixel size
            (Ignore if back_photo=False)
        back_photo : bool
            Set to True if want to return an array of background values, False
            to ignore anything to do with background

        Returns
        -------
        photometry of each star : array
        average background pixel value around each star : array (If back_photo=True)
        plots image with the aperture and centroids located for each star
        '''

        ax = self.frame.ax
        image = self.image
        pos = self.aperture_positions
        if len(pos) == 0:
            return None
        nstars = np.arange(0,np.shape(pos)[0],1)
        name_stars = []
        for i in nstars:
            name_stars.append('Star {}'.format(i))
        #print name_stars

        aperture = photutils.CircularAperture(pos,r=ap_size)

        if back_photo == True:
            back_aperture = photutils.CircularAnnulus(pos,r_in,r_out)

        pos = np.array(pos)



        for i in range(len(name_stars)):
            circle1 = plt.Circle((pos[i,0], pos[i,1]), ap_size, color='black',fill=False,zorder=100)
            ax.add_artist(circle1)
            plt.axhline(pos[i,1],xmin=pos[i,0]/100.-.01,xmax=pos[i,0]/100.+.02,color='black')
            plt.axvline(pos[i,0],ymin=pos[i,1]/100.-.01,ymax=pos[i,1]/100.+.02,color='black')
            plt.text(pos[i,0]+ap_size+1, pos[i,1], name_stars[i],zorder=11)
            #print pos[i,1]
            #print pos[i,0]

            if back_photo == True:
                circle2 = plt.Circle((pos[i,0], pos[i,1]), r_in, color='cyan',fill=False,zorder=10)
                circle3 = plt.Circle((pos[i,0], pos[i,1]), r_out, color='cyan',fill=False,zorder=10)
                ax.add_artist(circle2)
                ax.add_artist(circle3)
        #aperture.plot(origin=(0,0),indices=None,ax=ax,fill=False)
        #plt.ion()




        phot_table = photutils.aperture_photometry(image,aperture)
        flux_values = phot_table['aperture_sum'].data #gets a list of the total flux in specified aperture for each star

        if back_photo == True:
            back_table = photutils.aperture_photometry(image,back_aperture)
            area = np.pi*(r_out**2-r_in**2)
            a = np.ones((np.shape(image)[0],np.shape(image)[1]))
            area = photutils.aperture_photometry(a,back_aperture)
            back_values = back_table['aperture_sum'].data/area['aperture_sum'].data
            return flux_values,back_values*np.pi*ap_size**2
        else:
            return flux_values