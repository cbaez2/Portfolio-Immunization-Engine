# Portfolio Immunization Engine

## Overview

This project is a **deterministic Portfolio Immunization Engine** implemented in Python.

It computes **two asset cashflows**, `cf_x` and `cf_y`, that satisfy either **Full** or **Redington immunization conditions** at time `t = 0`, given:

- a user-selected immunization type (Full or Redington),
- a base interest rate `i0` at which the portfolio is immunized,
- a set of liability cashflow amounts,
- corresponding liability times, and
- exactly **two asset times**.

For **Redington immunization only**, the engine additionally computes an **interval of solvency**, defined as the set of interest rates for which the portfolio surplus remains non-negative.

For **both immunization types**, the engine supports **rebalancing under a change in interest rate to `i_n` and time to `t_n`**, recalculating the asset cashflows required to re-immunize the portfolio and reporting the resulting surplus at `i_n`.  
The **present values of the asset cashflows at `t = 0`** are also reported under their corresponding interest rates (`i_0` or `i_n`).

The project also includes a **graphical representation of the surplus function** \( S(i) \), allowing visualization of surplus behavior across interest rates for both Full and Redington immunization cases.

---

## Features

### Full Immunization

- Constructs asset cashflows that match liabilities satisfying the **Full immunization conditions**:
  - Present Value matching
  - Duration matching
  - **ALA (Asset–Liability–Asset)** cashflow structure.
- Recalculates asset cashflows required to re-immunize the portfolio under changes in interest rate `i_n` and time `t_n`, and reports the resulting surplus at `i_n`.

---

### Redington Immunization

- Constructs asset cashflows satisfying the **Redington immunization conditions**:
  - Present Value matching
  - Duration matching
  - Positive second derivative of the surplus function, `S''(i) > 0`
- Allows general asset–liability cashflow structures.
- Recalculates asset cashflows required to re-immunize the portfolio under changes in interest rate `i_n` and time `t_n`, and reports the resulting surplus at `i_n`.
- Computes a **finite interval of solvency** directly from the surplus function.

---

## Requirements
- Python 3.10+
- matplotlib
- numpy
- scipy
- sympy

### Install dependencies
```bash
pip install -r requirements.txt

```
## How to Run

1. Open `config.py` and set:
   - `IMMUNIZATION_TYPE` (`"full"` or `"redington"`)
   - Base inputs: `i0`, `liabilities`, `l_times`, `a_times`
   - Rebalancing inputs (optional): `i_n`, `t_n`

2. Run the program from the project root:
```bash

python main.py
```
---
  
##  Author

**Christopher Baez**  
Finance & Risk Management Major | Future Actuary  
Email: [chris_baez18@hotmail.com]  

---

## License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with proper attribution.
