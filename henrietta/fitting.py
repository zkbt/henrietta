import numpy as np, matplotlib.pyplot as plt
from astropy.modeling.core import Fittable1DModel, custom_model
from astropy.modeling.parameters import Parameter
from astropy.units import Quantity

from .modeling import BATMAN


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

    slope = delta/tau
    val_a = 1 - slope * (x - x1)
    val_b = 1 - delta
    val_c = 1 - slope * (x4 - x)
    result = np.select([range_a, range_b, range_c], [val_a, val_b, val_c], default=1)*baseline
    return result

BatmanTransit = custom_model(BATMAN)
