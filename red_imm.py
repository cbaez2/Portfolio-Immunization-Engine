import sympy as sp

#The program will determine the amount of 2  asset cashflows based their timing and the liabiltiies amount/timing following redington immunazation conditions

def red_immunization_two_cf(i0, a_times, liabilities, l_times):
    l_times = sorted(l_times)
    a_times = sorted(a_times)
    assert len(set(l_times)) == len(l_times), "Multiple liabilities at the same time are not allowed"  # this avoids cases like l_times=[2,2] since set(l_times) returns unique elements
    assert len(liabilities) == len(l_times), "The amount of liabilities and the liabilities times need to be equal"
    assert len(a_times) == 2, "Only two cashflows are allowed"
    assert all(t >= 0 for t in a_times), "Asset times must be ≥ 0 at t=0"
    assert all(t >= 0 for t in l_times), "Liability times must be ≥ 0 at t=0"
    assert i0 > 0, "Base interest rate must be positive"
    #defining mathematical variables and PV_A and PV_L functions of i

    i0= sp.nsimplify(i0) #saving exact value of i0

    x,y,i = sp.symbols('x,y,i')

    PV_A = x*(1+i)**-a_times[0] + y*(1+i)**-a_times[1]  # defining functions of i
    PV_L = sum(l*(1+i)**-t for l,t in zip(liabilities,l_times))

    #solving for cashflows
    cfs= sp.solve([
                PV_A.subs(i,i0) - PV_L.subs(i,i0),
                sp.diff(PV_A,i,1).subs(i,i0) - sp.diff(PV_L,i,1).subs(i,i0)], [x,y], dict=True)
    sol =cfs[0]
    x_val, y_val = sol[x], sol[y]

    #redefine PV_A with cfs found
    PV_A = x_val*(1+i)**-a_times[0] + y_val*(1+i)**-a_times[1]
    S  = PV_A - PV_L

    surplus_convexity = sp.diff(S,i,2).subs(i,i0)

    if surplus_convexity > 0:

        return {
            "cf_x" : x_val,
            "cf_y": y_val,
            "pv_x": x_val*(1+i0)**-a_times[0],
            "pv_y": y_val*(1+i0)**-a_times[1],
            "surplus_at_i0": S.subs(i,i0),
            "surplus_first_derivate_at_i0": sp.diff(S,i,1).subs(i,i0),
            "surplus_second_derivate_at_i0": surplus_convexity,
            "s(i)": S,
            "i0":i0
        }
    return {}

