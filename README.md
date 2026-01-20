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

The engine supports **rebalancing** after a given change in interest rate to i_n and/or time to t_n, and for Redington immunization it computes a **finite interval of solvency**, the set of interest rates for which the surplus remains non-negative.

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

## Requirements

- Python 3.10+
- sympy

## How to Run

1. Open `config.py`
2. Set the following parameters:
   - `IMMUNIZATION_TYPE` (`"full"` or `"redington"`)
   - Base model inputs: `i0`, `liabilities`, `l_times`, `a_times`
   - Rebalancing inputs: `t_n`, `i_n`
3. Run:

   
##  Author

**Christopher Baez**  
Finance & Risk Management Major | Future Actuary  
Email: [chris_baez18@hotmail.com]  

---

## License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with proper attribution.
