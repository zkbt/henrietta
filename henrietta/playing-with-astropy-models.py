from astropy.modeling import models, fitting, optimizers, statistic
import matplotlib.pyplot as plt, numpy as np


# In[48]:


# create a fake model
g = models.Gaussian1D()


# In[49]:


# create some fake data
x = np.linspace(-5, 5)
y = np.random.normal(g(x), 0.1)
plt.plot(x,y, '.')
plt.plot(x, g(x))


# In[50]:


# make a fitter
fitter = fitting.SimplexLSQFitter()
fitter(g, x, y)


# In[56]:


class VisualizedStatistic:
    '''
    Objects that inherit from VisualizedStatistic should be a drop-in
    replacement for the astropy.modeling.statistic.leastsq. The simplest
    class definiton that modifies this would simply be to redefine the
    `.name` attribute and the `.gof()` method.
    '''

    # this may appear in labels
    name = 'chisq'

    def __init__(self, fitter=None):
        self.fitter = fitter

    def gof(self, residuals):
        '''
        This calculates a goodness-of-fit from an array of residuals.
        (a lower value implies a better fit)

        Parameters
        ----------
        residuals : `~numpy.ndarray`
            Array of values for (data-model)/sigma

        Returns
        -------
        gof : float
            A single goodness-of-fit metric
            (in this case, sum of squares)
        '''
        return np.sum(residuals**2)

    def __call__(self, measured_vals, updated_model, weights, x, y=None):
        """
        Generic goodness-of-fit statistic.

        Parameters
        ----------
        measured_vals : `~numpy.ndarray`
            Measured data values.
        updated_model : `~astropy.modeling.Model`
            Model with parameters set by the current iteration of the optimizer.
        weights : `~numpy.ndarray`
            Array of weights to apply to each residual.
        x : `~numpy.ndarray`
            Independent variable "x" to evaluate the model on.
        y : `~numpy.ndarray`, optional
            Independent variable "y" to evaluate the model on, for 2D models.

        Returns
        -------
        res : float
            The sum of least squares.
        """

        if y is None:
            model_vals = updated_model(x)
        else:
            model_vals = updated_model(x, y)
        if weights is None:
            residuals = (model_vals - measured_vals)
        else:
            residuals = (weights * (model_vals - measured_vals))

        gof = self.gof(residuals)

        # plot the updated model on the data
        plt.sca(self.fitter.ax['data'])
        self.plotted['data']['models'].append(plt.plot(x, updated_model(x), color=color, alpha=alpha, **kw))
        plt.title('{} = {}'.format(self.name, gof))

        # plot the current step number and goodness of fit
        plt.sca(self.fitter.ax['gof'])
        self.fitter.steps += 1
        self.fitter.gof.append(gof)
        self.plotted['gof'].set_data(np.arange(self.fitter.steps), self.fitter.gof)

        # plot the current set of parameters on
        #plt.sca(self.fitter.ax['parameters'])

        return self.gof(residuals)

class VisualizedFitter(fitting.Fitter):
    '''
    Objects that inherit from a VisualizedFitter can do the normal
    stuff an astropy.fitting.Fitter can do, but they also visualize
    the process with panels that show:
    '''
    def visualize(self, model, x, y, *args, **kwargs):


        # set up a figure and some axes
        self.fi = plt.figure(figsize=(8, 5))
        self.gs = plt.matplotlib.gridspec.GridSpec(2, 2, height_ratios=[1, 2])

        # create some axes for our plot, and populate them with empty plots
        self.ax, self.plotted = {}, {}

        # create a space to plot the data vs. the model
        self.ax['data'] = plt.subplot(gs[1,0])
        self.ax['data'].set_xlabel('x')
        self.ax['data'].set_ylabel('y')
        self.plotted['data'] = dict(data=plt.scatter(x, y),
                                    intiial=plt.plot(x, model(x)))

        # create a space to plot the goodness-of-fit vs time
        self.ax['gof'] = plt.subplot(gs[1,1])
        self.ax['gof'].set_xlabel('Iteration')
        self.ax['gof'].set_ylabel('Goodness-of-Fit ({})'.format(self._stat_method.name))
        self.plotted['gof'] = plt.scatter([],[])

        return self.__call__(model, x=x, y=y, *args, **kwargs)

class test(fitting.SimplexLSQFitter, VisualizedFitter):
    pass


# In[46]:


f = test()
f._stat_method


# In[40]:


s = fitting.SimplexLSQFitter()
get_ipython().run_line_magic('pinfo2', 's.__call__')


# In[54]:


import astropy.modeling.statistic as stat
get_ipython().run_line_magic('pinfo2', 'stat.leastsquare')


# In[57]:


g.param_names
