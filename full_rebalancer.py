import sympy as sp
from full_imm import full_immunization_two_cf
from main import a_times, l_times, i0, liabilities


# ===============================
# FORMATTING HELPERS (REPORTING ONLY)
# ===============================

def r4(x):
    return round(float(sp.N(x)), 4)

def money(x):
    return f"${r4(x):,.4f}"

def rate(x):
    return f"{r4(x):.4f}"

def pv_at_i_n(cf, t_remaining, i_n):
    return cf * (1 + i_n) ** (-t_remaining)


# ===============================
# BASE FULL IMMUNIZATION SOLUTION
# ===============================

full_result = full_immunization_two_cf(
    i0=i0,
    a_times=a_times,
    liabilities=liabilities,
    l_times=l_times
)


def new_cfs(i_n, t_n):
    assert i_n > 0
    assert 0 <= t_n < a_times[1], "Must rebalance between t=[0, time of last asset)"

    x, y, i = sp.symbols('x,y,i')
    i_n = sp.nsimplify(i_n)

    # ===============================
    # CASE 0: t = 0 (rate shock only)
    # ===============================

    if t_n == 0:
        S_eval = full_result["s(i)"].subs(i, i_n)

        pv_x = pv_at_i_n(full_result["cf_x"], a_times[0], i_n)
        pv_y = pv_at_i_n(full_result["cf_y"], a_times[1], i_n)

        return (
            f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
            f"${r4(S_eval)}\n\n"
            f"To be fully immunized at iₙ = {rate(i_n)}, you need:\n"
            f"cf_x = {money(full_result['cf_x'])} at t = {a_times[0]} "
            f"(PV₀ = {money(pv_x)} @ iₙ)\n"
            f"cf_y = {money(full_result['cf_y'])} at t = {a_times[1]} "
            f"(PV₀ = {money(pv_y)} @ iₙ)"
        )

    # ===============================
    # CASE 1: 0 < t < first asset
    # ===============================

    elif 0 < t_n < a_times[0]:

        PV_A = x*(1+i)**-(a_times[0]-t_n) + y*(1+i)**-(a_times[-1]-t_n)
        PV_L = sum(l*(1+i)**-(t-t_n) for l, t in zip(liabilities, l_times))

        cfs = sp.solve([
            PV_A.subs(i, i_n) - PV_L.subs(i, i_n),
            sp.diff(PV_A, i, 1).subs(i, i_n)
            - sp.diff(PV_L, i, 1).subs(i, i_n)
        ], [x, y], dict=True)

        sol = cfs[0]
        x_val, y_val = sol[x], sol[y]

        PV_A = x_val*(1+i)**-(a_times[0]-t_n) + y_val*(1+i)**-(a_times[-1]-t_n)

        if (
            PV_A.subs(i, i_n) == PV_L.subs(i, i_n)
            and sp.diff(PV_A, i, 1).subs(i, i_n)
            == sp.diff(PV_L, i, 1).subs(i, i_n)
        ):
            pv_x = pv_at_i_n(x_val, a_times[0]-t_n, i_n)
            pv_y = pv_at_i_n(y_val, a_times[1]-t_n, i_n)

            return (
                f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
                f"${r4(full_result['s(i)'].subs(i, i_n))}\n\n"
                f"To restore full immunization at t = {t_n}, you need:\n"
                f"cf_x = {money(x_val)} at t = {a_times[0]} "
                f"(PV₀ = {money(pv_x)} @ iₙ)\n"
                f"cf_y = {money(y_val)} at t = {a_times[-1]} "
                f"(PV₀ = {money(pv_y)} @ iₙ)"
            )

        return (
            f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
            f"${r4(full_result['s(i)'].subs(i, i_n))}\n\n"
            f"Could not find cf_x at t = {a_times[0]} and cf_y at t= {a_times[1]} that satisfy full immunization "
            f"at t = {t_n} and iₙ = {rate(i_n)}."
        )

    # ===============================
    # CASE 2: first asset ≤ t < last asset
    # ===============================

    elif a_times[0] <= t_n < a_times[1]:

        PV_A = (
            full_result["cf_x"]*(1+i)**-(a_times[0]-t_n)
            + y*(1+i)**-(a_times[-1]-t_n)
        )

        PV_L = sum(l*(1+i)**-(t-t_n) for l, t in zip(liabilities, l_times))

        new_y_val = sp.solve(
            PV_A.subs(i, i_n) - PV_L.subs(i, i_n), y
        )[0]

        PV_A = (
            full_result["cf_x"]*(1+i)**-(a_times[0]-t_n)
            + new_y_val*(1+i)**-(a_times[1]-t_n)
        )

        if sp.diff(PV_A, i, 1).subs(i, i_n) == sp.diff(PV_L, i, 1).subs(i, i_n):

            pv_y = pv_at_i_n(new_y_val, a_times[1]-t_n, i_n)

            return (
                f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
                f"${r4(full_result['s(i)'].subs(i, i_n))}\n\n"
                f"You have already received {money(full_result['cf_x'])} at t = {a_times[0]}.\n"
                f"To restore full immunization at t = {t_n}, you need:\n"
                f"cf_y = {money(new_y_val)} at t = {a_times[1]} "
                f"(PV₀ = {money(pv_y)} @ iₙ)"
            )

        return (
            f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
            f"${r4(full_result['s(i)'].subs(i, i_n))}\n\n"
            f"Could not find a cf_y at t = {a_times[1]} that satisfies full immunization "
            f"at t = {t_n} and iₙ = {rate(i_n)}, given that "
            f"{money(full_result['cf_x'])} was already received at t = {a_times[0]}."
        )
