from ..fitting import *

def test_trapezoid():
    t = np.linspace(-1.5, 1.5, 10000)
    full = TrapezoidTransit()
    shortcut = customTrapezoidTransit()
    plt.plot(t, full(t), label='full', linewidth=3)
    plt.plot(t, shortcut(t), label='shortcut')
    plt.legend()
    plt.show()
