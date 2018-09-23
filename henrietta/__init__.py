'''
henrietta is a set of tools for playing with photometric light curves
in the Fall 2018 session of ASTR3400: Research Methods in Astronomy,
taught at CU Boulder by Zach Berta-Thompson (https://github.com/zkbt/).
'''

# for ASTR3400, let's use {semester}.{week}.{microversion}
__version__ = '0.4.1' 

# specify whether we're calling this from within setup.py
try:
    __HENRIETTASETUP__
except NameError:
    __HENRIETTASETUP__ = False

if not __HENRIETTASETUP__:
    # (run this stuff if it's not from within setup.py)

    def whoisthisawesomelady():

        print('''
        Henrietta Swan Leavitt (1868-1921) was an astronomer at the Harvard College
        Observatory. Her pioneering work in the study of variable stars allowed
        scientists to measure the size of the Universe for the first time.

        If you'd like to learn more about her, check out her
        [wikipedia page](https://en.wikipedia.org/wiki/Henrietta_Swan_Leavitt)
        or read some of
        [her papers](https://ui.adsabs.harvard.edu/#search/q=%20author%3A%22leavitt%2C%20henrietta%20swan).
        ''')

    from .lightcurves import *
    from .statistics import *
    from .modeling import *
    from .tools import *
