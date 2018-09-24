from ..fitting import *

def test_trapezoid():
    t = np.linspace(-1.5, 1.5, 10000)

    for tau in np.arange(4)*0.1:
        for T in np.arange(4)*0.1:
            model =  TrapezoidTransit(T=T, tau=tau)
            plt.plot(t, full(t), label=model.)
        #full = TrapezoidTransit()
        #triangle = TrapezoidTransit(tau=0.1, T=0.01)
        #shortcut = customTrapezoidTransit()
        #plt.plot(t, full(t), label='full', linewidth=3)
        #plt.plot(t, shortcut(t), label='shortcut')
        #plt.plot(t, triangle(t), label='triangle')

    plt.legend()
    plt.show()


def test_(N=1e6, duration=10, cadence=1.0/60.0/24.0, period=3.14, t0=0.5, **kw):
    lc = simulate_transit_data(N=N, duration=duration, cadence=cadence, period=period, t0=t0, **kw)
        plot_with_transit_model(lc, period=period, t0=t0, show_errors=e, **kw)

        folded = lc.fold(period=period, phase=t0/period)
        plot_with_transit_model(folded, period=period, t0=t0, show_errors=e, **kw)

    return lc, folded
