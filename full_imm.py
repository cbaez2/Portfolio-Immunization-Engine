import sympy as sp

#The program will determine the amount of 2  asset cashflows based their timing and the liabiltiies amount/timing following full immunazation conditions
#It is assumed that liabiltiies times and asset times are sorted in ascending order, it will be enforced anyway.

def full_immunization_two_cf(i0, a_times, liabilities, l_times):
    l_times= sorted(l_times)
    a_times = sorted(a_times)
    assert len(set(l_times)) == len(l_times), "Multiple liabilities at the same time are not allowed" #this avoids cases like l_times=[2,2] since set(l_times) returns unique elements
    assert len(liabilities) == len(l_times), "The amount of liabilities and the liabilities times need to be equal"
    assert len(a_times) == 2, "Only two cashflows are allowed"
    assert l_times[0] >= a_times[0] and l_times[-1] <= a_times[1], "ALA violation: liabilities must lie between asset times"
    assert i0>0

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

    conditions= S.subs(i, i0) == 0 and sp.diff(S, i, 1).subs(i, i0) == 0

    #case 1 deny exact matching. Ensure there are no liabilities occurs at the same time as both assets
    if len(liabilities)== 2 and l_times[0]==a_times[0]  and l_times[1]==a_times[1]:
        return {}
    #case 2 only one liability at the time of the first asset and return nothing if asset<liab
    if l_times[0] == a_times[0] and l_times[-1] != a_times[1] and x_val < liabilities[0]:
         return {}
    #case 3 only one liability at the time of the last asset and return nothing if asset<liab
    if l_times[-1] == a_times[1] and l_times[0] != a_times[0] and y_val < liabilities[-1]:
         return {}
    #case 4: At this point ALA is fully satisfied regardless of at most one liability at one asset time
    if conditions:
        return {
                "cf_x" : x_val,
                "cf_y": y_val,
                "pv_x": x_val*(1+i0)**-a_times[0],
                "pv_y": y_val*(1+i0)**-a_times[1],
                "surplus_at_i0": S.subs(i,i0),
                "s(i)": S,
                "i0":i0
        }
    #some unknown error occurs
    raise Exception