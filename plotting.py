import numpy as np
import matplotlib.pyplot as plt

def plot_surplus(
    S,
    i_min=0.0,
    i_max=5.0,
    S_min=-100.0,
    S_max=100.0,
    N=2000,
    title="Surplus Function"
):
    """
    Plot a numeric surplus function S(i).

    Parameters
    ----------
    S : callable
        Numeric surplus function S(i)
    i_min, i_max : float
        x-axis bounds for interest rate
    S_min, S_max : float
        y-axis bounds for surplus
    N : int
        Number of grid points
    title : str
        Plot title
    """

    i_vals = np.linspace(i_min, i_max, N)
    S_vals = np.array([S(i) for i in i_vals], dtype=float)

    plt.figure(figsize=(8, 5))
    plt.plot(i_vals, S_vals, label="S(i)")
    plt.axhline(0, linestyle="--", linewidth=1)

    plt.xlim(i_min, i_max)
    plt.ylim(S_min, S_max)

    plt.xlabel("Interest rate i")
    plt.ylabel("Surplus S(i)")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()
