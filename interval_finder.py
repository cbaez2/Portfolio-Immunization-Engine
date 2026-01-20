import sympy as sp
from red_imm import red_immunization_two_cf
from main import a_times, l_times, i0, liabilities

red_result = red_immunization_two_cf(
            i0=i0,
            a_times=a_times,
            liabilities=liabilities,
            l_times=l_times
        )

def interval_finder(S_i,i0):
    assert isinstance(S_i, sp.Expr), "Parameter must be a SymPy expression"
    i,r = sp.symbols('i,r')

    #finding simbolic roots
    s_roots= sp.solve(S_i.subs(i,r), r)

    #evaluaing symbolic roots
    n_roots = [root.evalf() for root in s_roots if root.is_real]

    #filtering roots
    roots_greater_than_i0 = sorted(list(x for x in n_roots if x > i0))
    roots_less_than_i0 = sorted(list(x for x in n_roots if x < i0 and x>0),reverse=True)

    #by default assume we are solvent for all i>0
    i_r= float('inf')
    i_l = 0

    #finding a root "i_r" to the right of i0 such that S(i_r) = 0 and S'(i_r) <0
    #note we are finding roots that are greater than i0 by default

    for root in roots_greater_than_i0:
        if sp.diff(S_i,i,1).subs(i,root)<0:
                i_r = root
                break

    #finding a root "i_l" to the left of i0 such that S(i_l) = 0 and S'(i_l) >0
    #note we are finding roots that are less than i0 by defualt

    for root in roots_less_than_i0:
        if sp.diff(S_i,i,1).subs(i,root) >0:
                i_l = root
                break

    return [i_l, i_r]
