from henrietta import *
plt.ion()

def test_batman():

    lc = create_photon_lightcurve(duration=10).normalize()
    transit_model(lc, period=1.0, Rp=0.3)
