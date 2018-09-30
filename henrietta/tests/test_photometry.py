from henrietta.photometry import *
import numpy as np
import matplotlib.pyplot as plt
import illumination as il

def test_photometry():
    seq = il.make_image_sequence(il.create_test_array(N=1, xsize=100, ysize=100, nstars=1, single=True, seed=0))
    illustration = il.imshowIllustration(seq)
    illustration.plot()
    ax = illustration.frames['image'].ax
    test = photometry(ax,seq[0],[[50,40]],ap_size=5)
