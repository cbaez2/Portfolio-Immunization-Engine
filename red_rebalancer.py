import sympy as sp
from red_imm import red_immunization_two_cf
from main import a_times, l_times, i0, liabilities

red_result = red_immunization_two_cf(
    i0=i0,
    a_times=a_times,
    liabilities=liabilities,
    l_times=l_times
)

# ===============================
# REPORTING HELPERS (ONLY)
# ===============================

def r4(x):
    return round(float(sp.N(x)), 4)

def money(x):
    return f"${r4(x):,.4f}"

def rate(x):
    return f"{r4(x):.4f}"

def pv_at_i_n(cf, t_remaining, i_n):
    return cf * (1 + i_n) ** (-t_remaining)


def new_cfs(i_n, t_n):
    assert i_n > 0
    assert 0 <= t_n < a_times[1], "Must rebalance between t = [0, time of last asset)"

    x, y, i = sp.symbols('x,y,i')
    i_n = sp.nsimplify(i_n)

    # ===============================
    # CASE 0: t_n = 0 - only interest rate change
    # ===============================

    if t_n == 0:
        #redington succeeds
        new_red_result = red_immunization_two_cf(i0=i_n, a_times=a_times, liabilities=liabilities, l_times=l_times) #new redington output at i_n
        if new_red_result:
            pv_x = pv_at_i_n(new_red_result["cf_x"], a_times[0], i_n)
            pv_y = pv_at_i_n(new_red_result["cf_y"], a_times[1], i_n)
            pv_total = pv_x + pv_y
            return(
                f"To restore Redington immunization at t = {t_n} under iₙ = {rate(i_n)}, you need:\n"
                f"cf_x = {money(new_red_result['cf_x'])} at t = {a_times[0]} "
                f"(PV₀ = {money(pv_x)} @ iₙ)\n"
                f"cf_y = {money(new_red_result['cf_y'])} at t = {a_times[1]} "
                f"(PV₀ = {money(pv_y)} @ iₙ)\n"
                f"TOTAL PV₀ (assets) = {money(pv_total)} @ iₙ\n\n"
                f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
                f"${sp.N(red_result['s(i)'].subs(i, i_n), 6)}"
            )

        #redington fails
        return(
            f"Could not find cf_x at t = {a_times[0]} and cf_y at t = {a_times[1]} "
            f"satisfying Redington immunization at t = {t_n} under iₙ = {rate(i_n)}.\n\n"
            f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
            f"${sp.N(red_result['s(i)'].subs(i, i_n), 6)}"
        )

    # ===============================
    # CASE 1: 0 < t_n < a_times[0]   - cf_x hasn't been paid so both cf_x and cf_y are unknown
    # ===============================

    elif 0 < t_n < a_times[0]:

        PV_A = (
            x*(1+i)**-(a_times[0]-t_n)
            + y*(1+i)**-(a_times[1]-t_n)
        )

        PV_L = sum(
            l*(1+i)**-(t-t_n) for l, t in zip(liabilities, l_times)
        )

        cfs = sp.solve([
            PV_A.subs(i, i_n) - PV_L.subs(i, i_n),
            sp.diff(PV_A, i, 1).subs(i, i_n)
            - sp.diff(PV_L, i, 1).subs(i, i_n)
        ], [x, y], dict=True)

        sol = cfs[0]
        x_val, y_val = sol[x], sol[y]

        PV_A = (
            x_val*(1+i)**-(a_times[0]-t_n)
            + y_val*(1+i)**-(a_times[1]-t_n)
        )

        S = PV_A - PV_L

        # redington succeeds
        if (
            S.subs(i, i_n) == 0
            and sp.diff(S, i, 1).subs(i, i_n) == 0
            and sp.diff(S, i, 2).subs(i, i_n) > 0
        ):
            pv_x = pv_at_i_n(x_val, a_times[0]-t_n, i_n)
            pv_y = pv_at_i_n(y_val, a_times[1]-t_n, i_n)
            pv_total = pv_x + pv_y

            return (
                f"To restore Redington immunization at t = {t_n} under iₙ = {rate(i_n)}, you need:\n"
                f"cf_x = {money(x_val)} at t = {a_times[0]} "
                f"(PV₀ = {money(pv_x)} @ iₙ)\n"
                f"cf_y = {money(y_val)} at t = {a_times[1]} "
                f"(PV₀ = {money(pv_y)} @ iₙ)\n"
                f"TOTAL PV₀ (assets) = {money(pv_total)} @ iₙ\n\n"
                f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
                f"${sp.N(red_result['s(i)'].subs(i, i_n), 6)}"
            )
        # redington fails
        return (
            f"Could not find cf_x at t = {a_times[0]} and cf_y at t = {a_times[1]} "
            f"satisfying Redington immunization at t = {t_n} under iₙ = {rate(i_n)}.\n\n"
            f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
            f"${sp.N(red_result['s(i)'].subs(i, i_n), 6)}"
        )

    # ===============================
    # CASE 2: a_times[0] ≤ t_n < a_times[1]  - finding cf_y given cf_x has already been paid.
    # ===============================

    elif a_times[0] <= t_n < a_times[1]:

        PV_A = (
            red_result["cf_x"]*(1+i)**-(a_times[0]-t_n)
            + y*(1+i)**-(a_times[1]-t_n)
        )

        PV_L = sum(
            l*(1+i)**-(t-t_n) for l, t in zip(liabilities, l_times)
        )

        new_y_val = sp.solve(
            PV_A.subs(i, i_n) - PV_L.subs(i, i_n), y
        )[0]

        PV_A = (
            red_result["cf_x"]*(1+i)**-(a_times[0]-t_n)
            + new_y_val*(1+i)**-(a_times[1]-t_n)
        )

        S = PV_A - PV_L

        # redington succeeds
        if (
            S.subs(i, i_n) == 0
            and sp.diff(S, i, 1).subs(i, i_n) == 0
            and sp.diff(S, i, 2).subs(i, i_n) > 0
        ):
            pv_y = pv_at_i_n(new_y_val, a_times[1]-t_n, i_n)
            pv_total = pv_y

            return (
                f"You have already received {money(red_result['cf_x'])} at t = {a_times[0]}.\n"
                f"To restore Redington immunization at t = {t_n} under iₙ = {rate(i_n)}, you need:\n"
                f"cf_y = {money(new_y_val)} at t = {a_times[1]} "
                f"(PV₀ = {money(pv_y)} @ iₙ)\n"
                f"TOTAL PV₀ (assets) = {money(pv_total)} @ iₙ\n\n"
                f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
                f"${sp.N(red_result['s(i)'].subs(i, i_n), 6)}"
            )

        # redington fails
        return (
            f"Could not find cf_y at t = {a_times[1]} satisfying Redington immunization "
            f"at t = {t_n} under iₙ = {rate(i_n)}, "
            f"given cf_x already received at t = {a_times[0]}.\n\n"
            f"The original surplus function evaluated at iₙ = {rate(i_n)} is:\n"
            f"${sp.N(red_result['s(i)'].subs(i, i_n), 6)}"
        )
