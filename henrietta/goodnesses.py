import numpy as np

def mean(residuals):
    '''
    Parameters
    ----------
    residuals : array
        Array of residuals = (data - model)/sigma

    Returns
    -------
    mean : float
        The mean of the residuals.
    '''

    return np.mean(residuals)

def votes(residuals=None):
    '''
    This is a goodness-of-fit function. It averages votes
    from user input, and then spits out a 1-10 score.

    Returns
    -------
    averagevote : float
        The average of a bunch of user-entered votes.
    '''

    # get input from the user
    answer = input('On a scale of 1-10, how good is this model?\n[separate multiple entries by commas]\n')

    # convert a string into numbers, and return its average
    average = np.mean([float(x) for x in answer.split(',')])

    # return that average out of the function
    return average
