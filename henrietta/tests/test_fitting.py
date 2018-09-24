from ..fitting import *

def test_trapezoid():
    t = np.linspace(-1.5, 1.5, 10000)

    for tau in np.arange(4)*0.1:
        for T in np.arange(4)*0.1:
            model =  TrapezoidTransit(T=T, tau=tau)
            plt.plot(t, model(t), label=repr(model))
    plt.legend()
    plt.show()


def test_(N=1e6, duration=10, cadence=1.0/60.0/24.0, period=3.14, t0=0.5, **kw):
    lc = simulate_transit_data(N=N, duration=duration, cadence=cadence, period=period, t0=t0, **kw)
    plot_with_transit_model(lc, period=period, t0=t0, show_errors=e, **kw)

    return lc, folded
