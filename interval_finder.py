import numpy as np
from scipy.optimize import brentq
from red_imm import red_immunization_two_cf
from main import a_times, l_times, i0, liabilities

red_result = red_immunization_two_cf(
    i0=i0,
    a_times=a_times,
    liabilities=liabilities,
    l_times=l_times
)

#  FIX 1: force numeric coefficients ONCE IF REDINGTON SUCEEDS
cf_x = float(red_result["cf_x"])
cf_y = float(red_result["cf_y"])



# ===============================
# SURPLUS FUNCTION (PURE NUMERIC)
# ===============================

def S(i):
    # domain guard (prevents nan / inf)
    if i <= -1:
        return np.nan

    v = 1.0 / (1.0 + i)

    PV_A = cf_x * v**a_times[0] + cf_y * v**a_times[1]
    PV_L = sum(float(L) * v**t for L, t in zip(liabilities, l_times))

    return float(PV_A - PV_L)


# ===============================
# NUMERIC DERIVATIVE
# ===============================

def dS(i, h=1e-6):
    return (S(i + h) - S(i - h)) / (2 * h)


# ===============================
# ROOT FINDER (ROBUST, SAFE)
# ===============================

def find_roots(i_min=0.0, i_max=5.0, N=4000):
    grid = np.linspace(i_min, i_max, N)
    vals = np.array([S(x) for x in grid], dtype=float)

    roots = []

    for x1, x2, f1, f2 in zip(grid[:-1], grid[1:], vals[:-1], vals[1:]):
        if not np.isfinite(f1) or not np.isfinite(f2):
            continue
        if f1 == 0.0:
            roots.append(x1)
        elif f1 * f2 < 0.0:
            try:
                roots.append(brentq(S, x1, x2))
            except ValueError:
                pass

    return sorted(set(roots))


# ===============================
# INTERVAL OF SOLVENCY (MY LOGIC)
# ===============================

def interval_finder(i0):
    roots = find_roots()

    roots_right = [r for r in roots if r > i0]
    roots_left  = [r for r in roots if 0 < r < i0][::-1]

    i_L = 0.0
    i_R = float("inf")

    # RIGHT bound: S(r)=0 AND decreasing
    for r in roots_right:
        if dS(r) < 0:
            i_R = r
            break

    # LEFT bound: S(r)=0 AND increasing
    for r in roots_left:
        if dS(r) > 0:
            i_L = r
            break

    return i_L, i_R
