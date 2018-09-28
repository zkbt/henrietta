from henrietta.photometry import *
from henrietta.phot.cartoons import *
import numpy as np
import matplotlib.pyplot as plt

ax = plt.subplot(111)
im = create_test_array(N=1, xsize=100, ysize=100, nstars=1, single=True,seed=None)

test = photometry(ax,im[0],[[50,40]],ap_size=5)
