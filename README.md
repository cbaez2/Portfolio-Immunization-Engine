# Portfolio Immunization Engine (Python)

## Overview

This project is a **deterministic Portofolio Immunization engine** implemented in Python using **SymPy**. that computes two asset cashflows satisfying full or Redington immunization conditions,

given:
- a base interest rate i0
- exactly **two asset times**,
- a fixed set of liability cashflow amounts,
- corresponding liability times, and

For Redington immunization, it additionally computes an **interval of solvency**, defined as the set of interest rates for which the surplus remains non-negative.
The engine recalculates asset cashflows needed to re-immunize the portflio given a change interest rate to `i_n` and time to `t_n`.  

---

## Features

### Full Immunization

- Matches:
  - Present Value
  - First derivative (duration)
- Enforces classical ALA constraints
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
