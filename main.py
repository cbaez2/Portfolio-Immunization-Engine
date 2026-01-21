import config

# ===============================
# EXTRACT USER VARIABLES
# ===============================

IMMUNIZATION_TYPE = config.IMMUNIZATION_TYPE.lower()
i0               = config.i0
liabilities      = config.liabilities
l_times          = config.l_times
a_times          = config.a_times
i_n              = config.i_n
t_n              = config.t_n

# ===============================
# FORMATTING HELPERS (REPORTING ONLY)
# ===============================

def r4(x):
    return round(float(x), 4)

def money(x):
    return f"${r4(x):,.4f}"

def rate(x):
    return f"{r4(x):.4f}"

def pv(cf, t, i):
    return cf * (1 + i) ** (-t)

def main():

# ===============================
# FULL IMMUNIZATION PIPELINE
# ===============================

    if IMMUNIZATION_TYPE == "full":
        from full_rebalancer import new_cfs, full_result

        print("\n=== FULL IMMUNIZATION ===\n")

        if full_result:
            cf_x = full_result["cf_x"]
            cf_y = full_result["cf_y"]

            pv_x_0 = pv(cf_x, a_times[0], i0)
            pv_y_0 = pv(cf_y, a_times[1], i0)
            pv_total_0 = pv_x_0 + pv_y_0   # ← ADDED

            print(
                f"Full immunization succeeded at t = 0 under i₀ = {rate(i0)}.\n\n"
                f"Liabilities:\n"
                f"  amounts = {liabilities}\n"
                f"  times   = {l_times}\n\n"
                f"Required asset cashflows:\n"
                f"  cf_x = {money(cf_x)} at t = {a_times[0]}  (PV₀ = {money(pv_x_0)} at i₀)\n"
                f"  cf_y = {money(cf_y)} at t = {a_times[1]}  (PV₀ = {money(pv_y_0)} at i₀)\n"
                f"  TOTAL PV₀ (assets) = {money(pv_total_0)} at i₀\n"
            )

            print("\n--- RE-IMMUNIZATION ---\n")
            print(new_cfs(i_n=i_n, t_n=t_n))

            from plotting import plot_surplus
            def S_full(i):
                if i <= -1:
                    return float("nan")
                v = 1.0 / (1.0 + i)
                PV_A = cf_x * v ** a_times[0] + cf_y * v ** a_times[1]
                PV_L = sum(L * v ** t for L, t in zip(liabilities, l_times))
                return PV_A - PV_L

            plot_surplus(
                S_full,
                title="Full Immunization Surplus S(i)"
            )

        if not full_result:   #No need to show graph
            print(
                f"Full immunization failed at t = 0 under i₀ = {rate(i0)}.\n"
                f"Liabilities: {liabilities} at times {l_times}\n"
                f"Asset times: {a_times}"
            )


    # ===============================
# REDINGTON IMMUNIZATION PIPELINE
# ===============================

    elif IMMUNIZATION_TYPE == "redington":
        from red_rebalancer import new_cfs, red_result
        from interval_finder import interval_finder

        print("\n=== REDINGTON IMMUNIZATION ===\n")

        if red_result:
            cf_x = red_result["cf_x"]
            cf_y = red_result["cf_y"]

            pv_x_0 = pv(cf_x, a_times[0], i0)
            pv_y_0 = pv(cf_y, a_times[1], i0)
            pv_total_0 = pv_x_0 + pv_y_0   # ← ADDED

            print(
                f"Redington immunization succeeded at t = 0 under i₀ = {rate(i0)}.\n\n"
                f"Liabilities:\n"
                f"  amounts = {liabilities}\n"
                f"  times   = {l_times}\n\n"
                f"Required asset cashflows:\n"
                f"  cf_x = {money(cf_x)} at t = {a_times[0]}  (PV₀ = {money(pv_x_0)} at i₀)\n"
                f"  cf_y = {money(cf_y)} at t = {a_times[1]}  (PV₀ = {money(pv_y_0)} at i₀)\n"
                f"  TOTAL PV₀ (assets) = {money(pv_total_0)} at i₀\n"
            )

            print("\n--- RE-IMMUNIZATION ---\n")
            print(new_cfs(i_n=i_n, t_n=t_n))

            print("\n--- INTERVAL OF SOLVENCY ---\n")
            interval_result = interval_finder(
                
                i0=red_result["i0"]
            )

            iL, iR = interval_result

            if iL == 0 and iR == float("inf"):
                print("S(i) ≥ 0  ∀  i ∈ [0, ∞)")
            elif iL != 0 and iR != float("inf"):
                print(f"S(i) ≥ 0  ∀  i ∈ [{iL}, {iR}]")
            elif iL == 0 and iR != float("inf"):
                print(f"S(i) ≥ 0  ∀  i ∈ (0, {iR}]")
            elif iL != 0 and iR == float("inf"):
                print(f"S(i) ≥ 0  ∀  i ∈ ({iL}, ∞)]")

            from plotting import plot_surplus

            def S_red(i):
                if i <= -1:
                    return float("nan")

                v = 1 / (1 + i)

                PV_A = cf_x * v ** a_times[0] + cf_y * v ** a_times[1]
                PV_L = sum(L * v ** t for L, t in zip(liabilities, l_times))

                return PV_A - PV_L

            plot_surplus(
                S_red,
                title="Redington Surplus S(i)"
            )

        if not red_result: #no need to show graph
            print(
                f"Redington immunization failed at t = 0 under i₀ = {rate(i0)}.\n"
                f"Liabilities: {liabilities} at times {l_times}\n"
                f"Asset times: {a_times}"
            )

    else:
        raise ValueError("IMMUNIZATION_TYPE must be 'full' or 'redington'")

if __name__ == "__main__":
    main()


