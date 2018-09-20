import numpy as np

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
