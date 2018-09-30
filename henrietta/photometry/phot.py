import numpy as np
import matplotlib.pyplot as plt
import photutils
import pdb


def photometry(ax,image,pos,ap_size=10):

    '''
    Create apertures around specified list of stars

    Parameters:
    -----------
    ax : axis class
        axis of a subplot.
    image : ndarray
        Image for aperture photometry to be performed on.
    pos : 2darray
        A list of positions in x,y pixel coordinates for each star.
        Needs to be as [[0,0],[1,1]...]
    ap_size : int
        The radius of a circular aperture in pixel size

    Returns
    -------
    photometry of each star : array
    plots image with the aperture and centroids located for each star
    '''

    nstars = np.arange(0,np.shape(pos)[0],1)
    name_stars = []
    for i in nstars:
        name_stars.append('Star {}'.format(i))
    print(name_stars)

    aperture = photutils.CircularAperture(pos,r=ap_size)

    pos = np.array(pos)


    #plt.imshow(image,origin='lower')

    for i in range(len(name_stars)):
        circle1 = plt.Circle((pos[i,0], pos[i,1]), ap_size, color='black',fill=False,zorder=100)
        ax.add_artist(circle1)
        plt.axhline(pos[i,1],xmin=pos[i,0]/100.-.01,xmax=pos[i,0]/100.+.02,color='black')
        plt.axvline(pos[i,0],ymin=pos[i,1]/100.-.01,ymax=pos[i,1]/100.+.02,color='black')
        plt.text(pos[i,0]+ap_size+1, pos[i,1], name_stars[i])
        print(pos[i,1])
        print(pos[i,0])

    #aperture.plot(origin=(0,0),indices=None,ax=ax,fill=False)
    plt.show()




    phot_table = photutils.aperture_photometry(image,aperture)
    flux_values = phot_table['aperture_sum'].data #gets a list of the total flux in specified aperture for each star

    return flux_values
