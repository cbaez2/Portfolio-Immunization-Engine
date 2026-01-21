# ==================================================
# USER-EDITABLE PARAMETERS
# ==================================================
# ONLY EDIT THIS FILE TO CHANGE MODEL BEHAVIOR
# ==================================================

# --------------------------------------------------
# IMMUNIZATION TYPE
# --------------------------------------------------
# Choose immunization method:
# "full"      → PV + Duration matching + ALA cashflow structure
# "redington" → PV + Duration + asset convexity > liability convexity
IMMUNIZATION_TYPE = "redington"


# --------------------------------------------------
# BASE INTEREST RATE
# --------------------------------------------------
# i0 : interest rate at which the asset portfolio is immunized
# Domain: i0 ≥ 0
i0 = 0.05


# --------------------------------------------------
# LIABILITY CASH FLOWS
# --------------------------------------------------
# - liabilities: liability amounts
# - l_times: corresponding liability times
# Constraints:
# - Same length
# - l_times sorted ascending
# - No duplicate liability times

liabilities = [1000, 1000, 1000, 1000, 1000]
l_times     = [0, 1, 2, 3, 4]

# Interpreted as: 1000 due at t=0,1,2,3,4 respectively


# --------------------------------------------------
# ASSET CASH FLOW TIMES
# --------------------------------------------------
# Specify asset cashflow times:
# - cf_x occurs at a_times[0]
# - cf_y occurs at a_times[1]
#
# Output:
# - cf_x, cf_y amounts and their present values
# - All PVs computed at t = 0 using i0

a_times = [1, 6]   # cf_x at t=1, cf_y at t=6


# --------------------------------------------------
# RE-IMMUNIZATION / EVALUATION PARAMETERS
# --------------------------------------------------
# i_n : new interest rate for re-immunization
#       Domain: (0, ∞)
#
# t_n : re-immunization time
#       Domain: 0 ≤ t_n < last asset time
#
# Output:
# - Adjusted asset cashflows (cf_x, cf_y) at t_n under i_n
# - PVs computed at t = 0 using i_n
# - If Redington: interval of solvency { i : S(i) ≥ 0 },
#   where S(i) = PV_A(i) − PV_L(i)

i_n = 0.50
t_n = 10

