import matplotlib.pyplot as plt, numpy as np
import matplotlib.animation as ani

from astropy.modeling import models, fitting, optimizers, statistic, custom_model
from .modeling import BATMAN
from tqdm import tqdm



BatmanTransit = custom_model(BATMAN)

@custom_model
def TrapezoidTransit(t, delta=0.01, P=1, t0=0, T=0.1, tau=0.01, baseline=1.0):

    """
    One dimensional Trapezoid Transit model,
    using the symbols defined for a circular
    transit approximation in Winn (2010).

    This is a fittable astropy model.

    Parameters
    ----------
    delta : float
        The depth of the transit, as a fraction of the out-of-transit flux.
    P : float
        The perio of the planet, in days.
    t0 : float
        Mid-transit time of the transit, in days.
    T : float
        The duration of the transit (from mid-ingress to mid-egress), in days.
    tau : float
        The duration of ingress/egress, in days.

    See Also
    --------
    astropy.modeling.models.Trapezoid1D

    Examples
    --------
    .. plot::
        :include-source:

        import numpy as np
        import matplotlib.pyplot as plt

        from henrietta.fitting import TrapezoidTransit

        plt.figure()
        model = TrapezoidTransit()
        t = np.arange(-5, 5, .01)

        for x in np.linspace(0.02, 0.2, 4):
            model.delta = x
            model.T = x
            plt.plot(t, model(t), lw=2)

        plt.show()
    """

    # calculate a phase-folded time (still in units of days)
    x = (t-t0 + 0.5*P) % P - 0.5*P

    # Compute the four points where the trapezoid changes slope
    # x1 <= x2 <= x3 <= x4

    if tau > T:
        x1 = -tau
        x2 = 0
        x3 = 0
        x4 = tau
    else:
        x1 = - (T+tau)/2.0
        x2 = - (T-tau)/2.0
        x3 = (T-tau)/2.0
        x4 = (T+tau)/2.0

    # Compute model values in pieces between the change points
    range_a = np.logical_and(x >= x1, x < x2)
    range_b = np.logical_and(x >= x2, x < x3)
    range_c = np.logical_and(x >= x3, x < x4)

    if tau == 0:
        slope = np.inf
    else:
        slope = delta/tau
    val_a = 1 - slope * (x - x1)
    val_b = 1 - delta
    val_c = 1 - slope * (x4 - x)
    result = np.select([range_a, range_b, range_c], [val_a, val_b, val_c], default=1)*baseline
    return result


def sumofsquares(residuals):
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

class VisualizedStatistic:
    '''
    Objects that inherit from VisualizedStatistic should be a drop-in
    replacement for the astropy.modeling.statistic.leastsq. The simplest
    class definiton that modifies this would simply be to redefine the
    `.name` attribute and the `.gof()` method.
    '''

    # this may appear in labels
    name = 'sumofsquares'

    def __init__(self, gof=sumofsquares, fitter=None):
        self.gof = gof
        self.fitter = fitter

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

        #print(self.fitter._iterations, gof)

        # plot the updated model on the data
        plt.sca(self.fitter.ax['data'])

        # make the previous model fade
        self.fitter.plotted['data']['models'][-1].set_alpha(0.3)
        self.fitter.plotted['data']['models'][-1].set_linewidth(1)
        self.fitter.plotted['data']['models'][-1].set_color('gray')


        # draw a new model line
        newline = plt.plot(x, updated_model(x), color='mediumseagreen', alpha=1, linewidth=3)[0]
        self.fitter.plotted['data']['models'].append(newline)

        plt.title('{} = {:.4}'.format(self.name, gof))

        # plot the current step number and goodness of fit
        plt.sca(self.fitter.ax['gof'])
        self.fitter._iterations += 1
        self.fitter._gof.append(gof)
        self.fitter.plotted['gof'].set_data(np.arange(self.fitter._iterations), self.fitter._gof)
        self.fitter.ax['gof'].set_xlim(0, self.fitter._iterations+1)
        self.fitter.ax['gof'].set_ylim(np.min(self.fitter._gof), np.max(self.fitter._gof))

        # update the parameters (kludge?)
        interesting = list(self.fitter.plotted['params'].keys())
        for i, p in enumerate(updated_model.param_names):
            if p in interesting:
                self.fitter._parameters[p].append(updated_model.parameters[i])
        # update the goodness
        self.fitter._parameters[self.name] = self.fitter._gof

        # update the plots
        for i, pi in enumerate(interesting):
            for j, pj in enumerate(interesting):
                x = self.fitter._parameters[pj]
                y = self.fitter._parameters[pi]
                if i>j:
                    #print(pj, x)
                    #print(pi, y)
                    #print('---')
                    self.fitter.plotted['params'][pi][pj].set_data((x, y))
                    if pi == self.name:
                        self.fitter.ax['params'][pi][pj].set_ylim(np.nanmin(y), np.nanmax(y))


        self.fitter.writer.grab_frame()
        print('Saving frame {} to {}.'.format(self.fitter._iterations, self.fitter.writer.outfile))

        return self.gof(residuals)


class VisualizedFitter(fitting.Fitter):
    '''
    Objects that inherit from a VisualizedFitter can do the normal
    stuff an astropy.fitting.Fitter can do, but they also visualize
    the process with panels that show:
    '''

    def __init__(self, optimizer=None, **kwargs):

        self.statistic = VisualizedStatistic(fitter=self)
        super().__init__(optimizer=optimizer, statistic=self.statistic)



    def visualize(self, model, x, y, filename='exploration.mp4', *args, **kwargs):

        fps = 30
        dpi = 200
        # figure out the writers to use
        if '.gif' in filename:
            try:
                writer = ani.writers['pillow'](fps=fps)
            except (RuntimeError, KeyError):
                writer = ani.writers['imagemagick'](fps=fps)
            except:
                raise RuntimeError('This python seems unable to make an animated gif.')
        else:
            try:
                writer = ani.writers['ffmpeg'](fps=fps)
            except (RuntimeError,KeyError):
                raise RuntimeError('This computer seems unable to ffmpeg.')
        self.writer = writer


        # restart our counter
        self._iterations = 0
        self._gof = []

        # set up a figure and some axes
        self.fi = plt.figure(figsize=(10, 7))
        gs = plt.matplotlib.gridspec.GridSpec(2, 2, height_ratios=[3, 1], hspace=0.25, wspace=0.2)

        # create some axes for our plot, and populate them with empty plots
        self.ax, self.plotted = {}, {}

        # create a space to plot the data vs. the model
        self.ax['data'] = plt.subplot(gs[0,0])
        self.ax['data'].set_xlabel('x')
        self.ax['data'].set_ylabel('y')
        self.plotted['data'] = dict(data=plt.plot(x, y, '.k', zorder=0),
                                    models=[plt.plot(x, model(x))[0]], zorder=-1)
        span = np.nanmax(y) - np.nanmin(y)

        self.ax['data'].set_ylim(np.nanmin(y)-span/2, np.nanmax(y)+span/2)


        # create a space to plot the goodness-of-fit vs time
        self.ax['gof'] = plt.subplot(gs[1,:])
        self.ax['gof'].set_xlabel('Iteration')
        self.ax['gof'].set_ylabel('Goodness-of-Fit\n({})'.format(self._stat_method.name))
        self.plotted['gof'] = plt.plot([],[], marker='o', color='mediumseagreen')[0]

        # create a space for plotting the parameters
        interesting = [p for p in model.param_names if model.fixed[p] == False]
        interesting += [self._stat_method.name]

        N = len(interesting)-1
        gs_param = plt.matplotlib.gridspec.GridSpecFromSubplotSpec(N, N, gs[0,1])
        self.ax['params'] = {p:{} for p in interesting}
        self.plotted['params'] = {p:{} for p in interesting}
        limits = dict( **model.bounds)
        limits[self._stat_method.name] = (0,1)
        for i, pi in enumerate(interesting):
            for j, pj in enumerate(interesting):
                if i>j:
                    ax = plt.subplot(gs_param[i-1,j])
                    self.ax['params'][pi][pj] = ax
                    ax.set_xlim(*limits[pj])
                    ax.set_ylim(*limits[pi])

                    #print(limits[pj], limits[pi])
                    if j == 0:
                        ax.set_ylabel(pi)
                    else:
                        plt.setp(ax.get_yticklabels(), visible=False)
                    if i == N:
                        ax.set_xlabel(pj)
                    else:
                        plt.setp(ax.get_xticklabels(), visible=False)

                    self.plotted['params'][pi][pj] = plt.plot([],[], '.', color='mediumseagreen')[0]

        self._parameters = {p:[] for p in interesting}

        with self.writer.saving(self.fi, filename, dpi or figure.get_dpi()):

            # actually do the fit (and populate the plots)
            fitted = self.__call__(model, x=x, y=y, *args, **kwargs)

        return fitted

class VisualizedSimplexFitter(fitting.SimplexLSQFitter, VisualizedFitter):
    pass

fitter = test()
model.ld1.fixed = True
model.ld2.fixed = True
model.period.fixed = True
model.t0.fixed = True


model.baseline.fixed = True
model.b.fixed=False
model.b.bounds = (0,1)
model.baseline.bounds = (0.99, 1.01)
model.a.bounds = (5, 15)
model.radius.bounds = (0.05, 0.15)

model.radius = 0.2
model.a = 5
model.b = 0.2
fitter.visualize(model, x, y)
fitter.ax['params']


def guessncheck(objfunc, model, N=100):

    best = model.parameters

    # create a best model
    tester = model.copy()


    # create empty array
    gof = np.ones(N)*np.inf

    # do a bunch of iterations
    for i in tqdm(range(N)):

        # set the parameters
        for w, p in enumerate(model.param_names):

            # only randomize bounded variables
            if None in model.bounds[p]:
                pass
            else:
                tester.parameters[w] = np.random.uniform(*model.bounds[p])

        # a little kludgy, but should work?
        gof[i] = objfunc(measured_vals=y,
                         updated_model=tester,
                         weights=None,
                         x=x)

        # store the best
        if gof[i] <= np.nanmin(gof):
            best = tester.parameters
            print(gof[i], tester.radius)

    return best

class VisualizedGuessNCheckFitter(VisualizedFitter):

    def __init__(self):
        super().__init__(optimizer=guessncheck, statistic=VisualizedStatistic)

    def __call__(self, model, x, y, N=100):

        # create a copy of the model
        model_copy = model.copy()

        # get the best fit parameters
        fitparams = self._opt_method(self._stat_method, model, N=N)
        model_copy.parameters = fitparams

        return model_copy

# make animate an option
# show the current best model every time
# write documentation that makes clear goodness must want to be minimized
# write wrapper that sets model bounds + fixed or not
# log axis for gof
# better default filename
# display mp4 in browswer
