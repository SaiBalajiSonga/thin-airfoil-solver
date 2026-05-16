# Thin Airfoil Theory Solver

A Python solver for 2D airfoil aerodynamics using **Thin Airfoil Theory (TAT)**. The airfoil is modelled as a distributed vortex sheet along its mean camber line, avoiding the need for full CFD. Developed for AE 244 — Assignment 2.

---

## Features

- Supports three airfoil modes: custom, NACA 4-digit, and novel airfoil comparison
- Computes Glauert–Fourier coefficients (A₀, A₁, A₂) via trapezoidal integration
- Calculates lift coefficient (Cₗ) and moment coefficients (Cₘ_c/4, Cₘ_LE)
- Visualises the velocity vector field over a 4c × 3c domain using Biot–Savart superposition
- Computes and plots the vortex strength distribution γ(θ) along the chord
- Verifies total circulation using two independent methods
- Plots pressure coefficient (Cₚ) distributions on upper and lower surfaces
- Flags high adverse pressure gradients as a simple stall indicator

---

## Requirements

- Python 3.10+
- NumPy
- Matplotlib

Install dependencies with:

```bash
pip install numpy matplotlib
```

---

## Getting Started

1. Clone the repository and navigate into it:

```bash
git clone http://github.com/SaiBalajiSonga/thin-airfoil-solver.git
cd thin-airfoil-solver
```

2. Run the solver:

```bash
python main.py
```

3. Select an airfoil mode when prompted:

```
1 → Custom camber airfoil
2 → NACA 4-digit airfoil
3 → Novel airfoil comparison (Section 4)
```

4. Enter the required inputs:

| Parameter | Symbol | Unit | Example |
|---|---|---|---|
| Maximum camber | m | — | 0.04 |
| Camber position | p | — | 0.4 |
| Angle of attack | α | degrees | 5 |
| Freestream velocity | U | m/s | 20 |
| Discretization points | N | — | 1000 |

> **Note:** m and p are not required for the custom airfoil mode (choice 1).  
> α is not prompted in novel comparison mode (choice 3) — a fixed sweep of [−3, 0, 3, 6, 9, 12]° is used instead.

---

## Outputs

### Printed to console

- Fourier coefficients: A₀, A₁, A₂
- Lift coefficient: Cₗ
- Moment coefficients: Cₘ_c/4 and Cₘ_LE
- Total circulation via vortex integration
- Total circulation via velocity line integral
- Maximum adverse pressure gradient (dCₚ/dx) on the upper surface

### Plots generated

1. **Camber Line** — geometry of the mean camber line
2. **Camber Slope** — local slope dyc/dx along the chord
3. **Velocity Vector Field** — flow around the airfoil in a 4c × 3c domain
4. **Vortex Strength Distribution** — γ(θ) along the chord (Kutta condition visible at TE)
5. **Pressure Distribution** — Cₚ on upper and lower surfaces at the given α
6. **Novel Camber Comparison** *(mode 3 only)* — overlaid camber lines for all four airfoils

---

## Customisation

### Custom airfoil shape (mode 1)

Edit the `custom_airfoil(x)` function in `camber.py`:

```python
def custom_airfoil(x):
    y = 0.05 * np.sin(np.pi * x)
    return y
```

The slope is computed automatically via central-difference numerical differentiation.

> **Constraint:** the function must satisfy `yc(0) = 0` and `yc(1) = 0`, otherwise TAT will produce incorrect results.

### Novel airfoil shapes (mode 3)

Edit the `Novel_camber_functions(x)` function in `camber.py`:

```python
def Novel_camber_functions(x):
    yc1 = 0.08 * np.sin(np.pi * x)
    yc2 = 0.05 * (np.sqrt(np.maximum(x, 0)) - x)
    yc3 = 0.02 * np.sin(2 * np.pi * x)
    return yc1, yc2, yc3
```

The same boundary condition applies: `yc(0) = 0` and `yc(1) = 0`.

---

## Technical Notes

- Chord length is normalised to c = 1
- Cosine (Glauert) spacing is used for improved leading and trailing edge resolution
- Midpoint vortex sampling avoids singularities in the induced velocity calculation
- The Biot–Savart law is applied discretely for the velocity field
- Linearised Bernoulli equation is used for pressure coefficient estimation
- Positive angle of attack produces positive lift

---

## File Structure

```
.
├── main.py             # Central program controller
├── user_input.py       # Console input collection
├── camber.py           # Camber line geometry and slope computation
├── fourier.py          # Fourier coefficients and aerodynamic coefficients
├── velocity_field.py   # Velocity field and pressure distribution (Biot–Savart)
├── circulation.py      # Circulation verification via line integral
├── plotting.py         # All visualisation functions
└── README.md
```

---

## Theory Background

This solver implements the classical **Glauert thin airfoil theory**, where the camber line boundary condition is satisfied using a Fourier vortex sheet:

$$\gamma(\theta) = 2U \left[ A_0 \frac{1 + \cos\theta}{\sin\theta} + \sum_{n=1}^{\infty} A_n \sin(n\theta) \right]$$

The lift and moment coefficients follow from the first three Fourier terms:

$$C_l = \pi(2A_0 + A_1), \qquad C_{m_{c/4}} = -\frac{\pi}{4}(A_1 - A_2)$$