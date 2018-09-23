import numpy as np, matplotlib.pyplot as plt
from astropy.modeling.core import Fittable1DModel
from astropy.modeling.parameters import Parameter
from astropy.modeling.models import custom_model
from astropy.units import Quantity

class TrapezoidTransit(Fittable1DModel):
    """
    One dimensional Trapezoid Transit model,
    using the symbols defined for a circular
    transit approximation in Winn (2010).

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
            plt.plot(r, model(r), lw=2)

        plt.show()
    """

    inputs = ('t',)
    outputs = ('y',)

    delta = Parameter(default=0.01)
    P = Parameter(default=1.0)
    t0 = Parameter(default=0.0)
    T = Parameter(default=0.1)
    tau = Parameter(default=0.01)
    baseline = Parameter(default=1.0)

    @staticmethod
    def evaluate(t, delta, P, t0, T, tau, baseline):
        """
        One dimensional Trapezoid transit model function.
        The parameters are interpreted as the same order
        with which they were added to the model (?).
        """

        # calculate a phase-folded time (still in units of days)
        x = (t-t0 + 0.5*P) % P - 0.5*P

        # Compute the four points where the trapezoid changes slope
        # x1 <= x2 <= x3 <= x4

        x1 = - (T+tau)/2.0
        x2 = - (T-tau)/2.0
        x3 = (T-tau)/2.0
        x4 = (T+tau)/2.0

        # Compute model values in pieces between the change points
        range_a = np.logical_and(x >= x1, x < x2)
        range_b = np.logical_and(x >= x2, x < x3)
        range_c = np.logical_and(x >= x3, x < x4)


        slope = delta/tau
        val_a = 1 - slope * (x - x1)
        val_b = 1 - delta
        val_c = 1 - slope * (x4 - x)
        result = np.select([range_a, range_b, range_c], [val_a, val_b, val_c], default=1)*baseline

        if isinstance(baseline, Quantity):
            return Quantity(result, unit=baseline.unit, copy=False)
        else:
            return result


    @property
    def input_units(self):
        if self.P.unit is None:
            return None
        else:
            return {'x': self.P.unit}

    def _parameter_units_for_data_units(self, inputs_unit, outputs_unit):

        delta = Parameter(default=0.1)
        P = Parameter(default=1.0)
        t0 = Parameter(default=0.0)
        T = Parameter(default=0.1)
        tau = Parameter(default=0.01)
        baseline = Parameter(default=1.0)


        return OrderedDict([('delta', None),
                            ('P', inputs_unit['x']),
                            ('t0', inputs_unit['x']),
                            ('T', inputs_unit['x']),
                            ('tau', inputs_unit['x']),
                            ('baseline', outputs_unit['y'])])

@custom_model
def customTrapezoidTransit(t, delta=0.01, P=1, t0=0, T=0.1, tau=0.01, baseline=1.0):

    """
    This does the same thing as the TrapezoidTransit class above. It's a
    slightly simpler way of defining a custom model. It's a little less
    flexible (I think), but for most purposes this should be a reasonable
    template to work from.
    """

    # calculate a phase-folded time (still in units of days)
    x = (t-t0 + 0.5*P) % P - 0.5*P

    # Compute the four points where the trapezoid changes slope
    # x1 <= x2 <= x3 <= x4

    x1 = - (T+tau)/2.0
    x2 = - (T-tau)/2.0
    x3 = (T-tau)/2.0
    x4 = (T+tau)/2.0

    # Compute model values in pieces between the change points
    range_a = np.logical_and(x >= x1, x < x2)
    range_b = np.logical_and(x >= x2, x < x3)
    range_c = np.logical_and(x >= x3, x < x4)

    slope = delta/tau
    val_a = 1 - slope * (x - x1)
    val_b = 1 - delta
    val_c = 1 - slope * (x4 - x)
    result = np.select([range_a, range_b, range_c], [val_a, val_b, val_c], default=1)*baseline
    return result
