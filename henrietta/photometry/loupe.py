import illumination as il
from ..imports import *
from .apertures import *
from ..imaging import io

from IPython.display import display
from astropy.table import vstack
import ipywidgets as widgets

# Check it out:
# https://github.com/matplotlib/jupyter-matplotlib might be good for widgets!


class Loupe(il.IllustrationBase):
    '''
    An interactive Illustration, that allows us to do
    aperture photometry on particular locations in an image.
    '''
    illustrationtype = 'Loupe'

    def create_frame(self, *args, **framekw):
        '''
        (part of __init__)
        Create the illustration frame.
        '''
        plt.ioff()

        # figure out the geometry, for the figure
        aspectratio = self.image.shape[1]/float(self.image.shape[0])
        width = 5
        height = width/aspectratio
        #if aspectratio >=1:
        #    width = size*aspectratio
        #    height = size
        #else:
        #    width = size
        #    height = size/float(aspectratio)

        # create the basic illustration layout (this creates a self.grid)
        il.IllustrationBase.__init__(self, 1, 1,
                                  figkw=dict(figsize=(width, height), dpi=100),
                                  hspace=0.02, wspace=0.02,
                                  left=0.05, right=0.95,
                                  bottom=0.1, top=0.9)
        self._pithy = True

        # create an imshowFrame to display the image (and hide its text output)
        self.frames['imshow'] = il.imshowFrame(data=self.images, illustration=self, **framekw)
        self.frames['imshow']._pithy=True

        # create an ax for this frame
        self.frames['imshow'].ax = plt.subplot(self.grid[0, 0])


        # draw this illustration
        self.plot()

    def create_widgets(self, maxaperture=50):
        '''
        (part of __init__)
        Create the control widgets for interactions.
        '''

        ####################################
        # create the aperture radius control
        ####################################

        # a label for setting the aperture
        aperture_radius_label = widgets.Label('Photometric Aperture')

        # a slider to pick the radius of the aperture
        aperture_radius_slider = widgets.IntSlider(
                                    value=self.aperture_radius,
                                    min=0,
                                    max=maxaperture,
                                    step=1,
                                    description='Radius',
                                    orientation='horizontal',
                                    continuous_update=False,
                                    readout=True,
                                    layout={'width':'100%'})

        # make the combined aperture widget
        self.aperture_widget = widgets.VBox([aperture_radius_label,
                                             aperture_radius_slider])

        ###########################################
        # create the background subtraction control
        ###########################################

        # a checkbox to decide if we should subtract the background
        background_checkbox = widgets.Checkbox(
                                        value=False,
                                        description='Subtract Background?',
                                        disabled=False)

        # a label for the background subtraction
        background_label = widgets.Label('Background Subtraction',
                                         disabled=True)

        # a range slider to pick the inner + outer radii of the annulus
        background_slider = widgets.IntRangeSlider(
                                value=[2*self.aperture_radius,
                                       3*self.aperture_radius],
                                min=0,
                                max=100,
                                step=1,
                                description='Radii',
                                disabled=True,
                                continuous_update=False,
                                orientation='horizontal',
                                readout=True,
                                layout={'width':'100%'})

        # only turn on the background slider if we need it
        def update_background_slider(checkbox):
            '''
            What do we do when the background checkbox is updated?
            '''
            do_background = checkbox['new'] == False
            background_slider.disabled = do_background
        background_checkbox.observe(update_background_slider, names='value')

        # don't let the background inner radius go inside the aperture radius
        widgets.jslink((aperture_radius_slider, 'value'),
                       (background_slider, 'min'))

        # create the combined background widget
        self.background_widget = widgets.VBox([background_label,
                                               background_checkbox,
                                               background_slider])


        # set up the interaction loop
        self.widge = widgets.interactive(self.photometry,
                                         aperture_radius=aperture_radius_slider,
                                         background_radii=background_slider,
                                         subtract_background=background_checkbox)

        #self.window = widgets.Output(layout={'border': '1px solid black', 'width':'70%', 'height':'500px'})
        self.output_widget = widgets.Output(layout={'border': '1px solid black',
                                                    'margin': '1% 0% 1% 0%',
                                                    'height':'100px'})



        self.instruction_widget = widgets.Output(layout={'border': '1px solid black',
                                                        'margin': '1% 0% 1% 0%',
                                                        'height':'40px',
                                                        'background_color':'red',
                                                        })

    def __init__(self, image,
                       aperture_radius=10.0,
                       subtract_background = False,
                       **framekw):
        '''
        Parameters
        ----------

        image : 2D array, str
            An image or a path to a filename containing an image.

        aperture_radius : float
            The default radius for the photometric aperture
            (can be changed interactively).

        subtract_background : bool
            Should we attempt to do background subtraction?
            (not fully implemented yet)

        **framekw passed to CameraFrame
        '''

        # load an image if given a filename
        if type(image) == str:
            image = io.read_image(image)

        self.images = il.make_image_sequence(image)

        # don't let this illustration talk
        self._pithy = True

        # store the image as an attribute of the loupe
        self.image = image


        # store the initial defaults
        self.aperture_radius = aperture_radius
        self.subtract_background = subtract_background

        # start with no apertures
        self.apertures = []
        self.napertures = 0


        self.create_widgets()



        with self.instruction_widget:
            print("Please [a]dd or [z]ap an aperture at the cursor location.")

        # display the widgets


        controls = widgets.VBox([self.aperture_widget, self.background_widget],
                                        layout=dict(width='35%',
                                                    margin='0% 3% 0% 0%'))

        #plot = widgets.HBox([self.figure.canvas], layout={'width':'500px',
        #                                                'height':'500px',})


        self.create_frame()
        image = widgets.VBox([self.figure.canvas],
                             layout=dict(width='62%',
                                         margin='0% 3% 0% 0%'))

        interaction = widgets.HBox([controls, image])

        layout = widgets.VBox([self.instruction_widget,
                               interaction,
                               self.output_widget])




        display(layout)

        # set it up so we can add or subtract an aperture by clicking on the image
        self.figure.canvas.mpl_connect('key_press_event', self.do_something_with_keyboard)

        # (for better layout, is it possible to place the matplotlib notebook
        #  plot *inside* a widget Output? that way, I could set the layout
        # for the output to decide where the plot goes

    def do_something_with_keyboard(self, event):
        '''
        If the user clicks on the imshow, do something with that click.

        Parameters
        ----------
        event : matplotlib.backend_bases.LocationEvent
        '''
        self.lastevent = event
        if event.key.lower() == 'z':
            self.remove_aperture(event.xdata, event.ydata)
        elif event.key.lower() == 'a':
            self.add_aperture(event.xdata, event.ydata)
        plt.draw()
        self.widge.update()

    def add_aperture(self, x, y):
        '''
        Add an aperture at a particular (x, y) location.
        '''
        #with self.out:
        #    print('adding aperture at {}'.format((x,y)))
        position = np.array([x,y])
        name = 'Star {}'.format(self.napertures)

        new = InteractiveAperture(name=name,
                                  pos=position,
                                  loupe=self,
                                  aperture_radius=self.aperture_radius)
        # plot this aperture on the image
        new.plot(ax=self.frames['imshow'].ax)

        # store this new aperture in a list
        self.apertures.append(new)
        self.napertures += 1

    def remove_aperture(self, x, y):
        '''
        Remove the closest aperture to the given (x,y) location.

        Parameters
        ----------
        x, y : float
            The location where we want to remove an aperture.
        '''
        #with self.out:
        #    print('removing aperture from {}'.format((x,y)))
        positions = [a.positions[0] for a in self.apertures]
        xexisting, yexisting = np.array(positions).T
        distance = (xexisting - x)**2 + (yexisting - y)**2
        closest = np.argmin(distance)

        toremove = self.apertures.pop(closest)
        toremove.erase()


    def photometry(self, aperture_radius=10,r_in=20,r_out=30,back_photo=True):

        '''
        Create apertures around specified list of stars

        Parameters:
        -----------

        aperture_radius : float
            The radius of a circular aperture in pixel size
        r_in : float
            The inner radius of background aperture in pixel size
            (Ignore if back_photo=False)
        r_out : float
            The outer radius of background aperture in pixel size
            (Ignore if back_photo=False)

        Returns
        -------
        photometry of each star : array
        average background pixel value around each star : array (If back_photo=True)
        plots image with the aperture and centroids located for each star
        '''

        # if we have no apertures, do nothing
        if len(self.apertures) == 0:
            return None

        # pull out the plotting ax and the image
        ax = self.frames['imshow'].ax
        image = self.image

        self.aperture_radius = aperture_radius

        #if back_photo == True:
        #    back_aperture = photutils.CircularAnnulus(pos,r_in,r_out)

        for i, a in enumerate(self.apertures):
            a.update()


        #if back_photo == True:
        #    back_table = photutils.aperture_photometry(image,back_aperture)
        #    area = np.pi*(r_out**2-r_in**2)
        #    a = np.ones((np.shape(image)[0],np.shape(image)[1]))
        #    area = photutils.aperture_photometry(a,back_aperture)
        #    back_values = back_table['aperture_sum'].data/area['aperture_sum'].data
        #    return flux_values,back_values*np.pi*aperture_radius**2
        #else:
        self.output_widget.clear_output()
        with self.output_widget:
            self.summarize()
        self.measurements = vstack([a.phot_table for a in self.apertures])
        self.measurements['name'] = [a.name for a in self.apertures]
        self.measurements = self.measurements['name','xcenter', 'ycenter', 'aperture_sum']

        plt.draw()

        return self.measurements

    def summarize(self):
        print('With r={}px apertures:'.format(self.aperture_radius))
        for a in self.apertures:
            print(' {}'.format(a))
