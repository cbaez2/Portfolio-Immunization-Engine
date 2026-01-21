# Portfolio Immunization Engine

## Overview

This project is a **deterministic Portfolio Immunization Engine** implemented in Python.

It computes **two asset cashflows**, `cf_x` and `cf_y`, that satisfy either **Full** or **Redington immunization conditions** at time `t = 0`, given:

- a user-selected immunization type (Full or Redington),
- a base interest rate `i0` at which the portfolio is immunized,
- a set of liability cashflow amounts,
- corresponding liability times, and
- exactly **two asset times** for `cf_x` and `cf_y`.

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
# How to Run the Project (Quick Start – Windows)

This guide explains how to run the project locally using **Windows** with minimal setup.

---

## 1. Install Python (Required)

Before running the project, Python must be installed.

1. Go to **https://www.python.org**
2. Download **Python 3.x** for Windows.
3. During installation, **check the box labeled “Add Python to PATH”**.
4. Complete the installation.

Verify Python is installed by opening a terminal and running:

```bash
python --version
```

## 2. Download the Project

1. Go to the GitHub repository.
2. Click the green **`<> Code`** button.
3. Select **Download ZIP**.
4. Extract the ZIP file to any location on your computer (e.g. `Documents`).

---

## 3. Open the Project in the Terminal

1. Open the extracted project folder.
2. Right-click on an empty area inside the folder.
3. Select **“Open in Terminal”** or **“Open Command Prompt here”**  
   (the wording depends on your Windows version).

A terminal window should now open **at the project directory**.

---

## 4. (One-Time) Install Dependencies

From the terminal run:

```bash
pip install -r requirements.txt
```
## 5. Configure Model Inputs

All user-editable inputs are controlled through **`config.py`**.

1. Open `config.py` using any text editor (Notepad, VS Code, etc.).
2. Modify the parameters, including:
   - immunization type (Full or Redington),
   - base interest rate,
   - asset times,
   - liability amounts and their corresponding times.
3. Save the file after making changes.

No other files need to be edited.

## 6. Run the Program

From the terminal, run:

```bash
python main.py

```
# You must close the image file to re-run the engine.
---
  
##  Author

**Christopher Baez**  
Finance & Risk Management Major | Future Actuary  
Email: [chris_baez18@hotmail.com]  

---

## License

This project is licensed under the **MIT License** — you are free to use, modify, and distribute it with proper attribution.
