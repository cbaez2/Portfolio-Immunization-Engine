# Asset–Liability Immunization Engine (Python)

## Overview

This project is a **deterministic Asset–Liability Immunization engine** implemented in Python using **SymPy**.

Given:
- a base interest rate i0
- a fixed set of liability cashflow amounts,
- corresponding liability times, and
- exactly **two asset times**,

the program computes the **two asset cashflows** required to achieve either:

- **Full Immunization**, or
- **Redington Immunization**.

The engine also supports **rebalancing** after:
- a change in interest rate, and/or
- a change of time.

For **Redington Immunization**, the engine additionally computes a **finite interval of solvency**, a set of interest rates for which the surplus remains non-negative.
---

## Features

### Full Immunization

- Matches:
  - Present Value
  - First derivative (duration)
- Enforces classical ALA constraints
- Computes exact asset cashflows symbolically
- Supports rebalancing at arbitrary time `t_n` and interest rate `i_n`

---

### Redington Immunization

- Matches:
  - Present Value
  - Duration
  - Positive second derivative (convexity)
- Allows liabilities outside the asset interval
- Supports rebalancing at arbitrary time `t_n` and interest rate `i_n`
- Computes a **finite interval of solvency** directly from the surplus function

---

## Example Output

A typical run reports:

- Initial immunization success
- Required asset cashflows
- Present values at time 0
- Rebalancing requirements after a rate shock
- Interval of solvency (Redington only)

Example excerpt:

=== REDINGTON IMMUNIZATION ===

Redington immunization succeeded at i₀ = 0.1000

Liabilities:
  amounts = [1000, 1000, 1000, 1000, 1000]
  times   = [0, 1, 2, 3, 4]

Required asset cashflows:
  cf_x = $3,843.6664 at t = 1  (PV₀ = $3,494.2422 at i₀)
  cf_y = $1,196.9078 at t = 6  (PV₀ = $675.6232 at i₀)


--- REBALANCING ---

The original surplus function evaluated at iₙ = 0.5000 is:
$62.5843

To be Redington immunized at iₙ = 0.5000 and t = 0, you need:
cf_x = $3,843.6664 at t = 1 (PV₀ = $2,562.4443 @ iₙ)
cf_y = $1,196.9078 at t = 6 (PV₀ = $105.0783 @ iₙ)

--- INTERVAL OF SOLVENCY ---

S(i) ≥ 0  ∀  i ∈ (0, 1.01475833214883]

# How to Run

1. Open `main.py`
2. Set:
   - `IMMUNIZATION_TYPE`
   - `i0`, `liabilities`, `l_times`, `a_times`
   - Rebalancing parameters `t_n` and `i_n`
3. Run:
   
##  Author

**Christopher Baez**  
Finance & Risk Management Major | Future Actuary  
Email: [chris_baez18@hotmail.com]  

---

## License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with proper attribution.
